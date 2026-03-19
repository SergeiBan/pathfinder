from django.shortcuts import render, redirect
from .forms import SeaCalculationForm, RRCalculationForm, SeaRRCalculationForm, UploadForm
from .models import (
    SeaCalculation, SeaRate, InnerRRRate, LocalHubCity, SeaEndTerminal, InnerRRTerminal,
    DistantTruckRate, SeaStartTerminal, SeaLine, SeaETD, ACCEPTABLE_POLS, ACCEPTABLE_AGENTS
)
from .utils import (
    get_line_mm_rates, get_agent_mm_rates, find_seapath, find_all_seapaths, get_pol,
    get_carrier, get_pods, get_etd, get_container_prices, make_dates, get_conversion,
    check_agent
)
from django.db.models import F
from django.http import Http404
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
import pandas as pd
import datetime

from .parse_rates import parse_for


def index(request):
    return redirect('paths:sea_rr_calculation')


def sea_calculation(request):
    form = SeaCalculationForm(request.POST or None)

    if form.is_valid():
        form.save()

    context = {
        'form': form
    }

    return render(request, 'paths/sea_calculation.html', context)


def rr_calculation(request):
    form = RRCalculationForm(request.POST or None)

    if form.is_valid():
        form.save()

    context = {
        'form': form
    }

    return render(request, 'paths/rr_calculation.html', context)


def sea_rr_calculation(request):
    form = SeaRRCalculationForm(request.POST or None)
    direct_sea_rates = None
    sea_truck = None

    line_rates = None 
    line_sea_rr_truck = None

    agent_rates = None
    agent_sea_rr_truck = None

    end_terminals = None
    remote_truck_rates = None
    sea_truck = []
    
    if form.is_valid():
        end_city = form.cleaned_data['end_city']
        particular_rr_terminal = form.cleaned_data['rr_end_terminal']
        
        # Если выбран конкретный ЖД терминал прибытия
        if particular_rr_terminal:
            end_terminals = InnerRRTerminal.objects.filter(pk=form.cleaned_data['rr_end_terminal'].pk)
        else:
            end_terminals = end_city.rr_terminals.all()
        
        # 1. Получаем все морские ставки из терминала отправления во все российские терминалы
        sea_rates = find_all_seapaths(
            form.cleaned_data['sea_start_terminal'],
            form.cleaned_data['container'],
            SeaRate,
            form.cleaned_data['etd_from'],
            form.cleaned_data['etd_to']
        )

        # 1.1 Если не нашлось ставок. НУЖНО БУДЕТ добавить сообщение для пользователей!
        if not sea_rates:
            context = {
            'form': form,
            }
            return render(request, 'paths/sea_rr_calculation.html', context)

      
        # 2 Делим морские ставки на линейные и агентские
        agent_sea_rates = sea_rates.filter(agent__isnull=False)
        line_sea_rates = sea_rates.filter(agent__isnull=True)
        
        line_rates, line_sea_rr_truck = get_line_mm_rates(
            line_sea_rates, InnerRRRate, end_terminals, form.cleaned_data['container'], end_city)
        
        agent_rates, agent_sea_rr_truck = get_agent_mm_rates(
            agent_sea_rates, InnerRRRate, end_terminals, form.cleaned_data['container'], end_city)


        # 3. Вдруг возможен автовывоз из портового города в конечный город
        if end_city.ingoing_truck_rates.exists():
            remote_truck_rates = end_city.ingoing_truck_rates.all()
            
            # Сопоставляем морские ставки и ставки автовывоза по городу,
            # если возможен автовывоз из портового горада, минуя ЖД
            for sea_rate in sea_rates:
                for truck_rate in remote_truck_rates:
                    if sea_rate.sea_end_terminal.local_hub_city == truck_rate.start_city:
                        sea_truck.append([sea_rate, truck_rate])

        # 4. Проверям, что пункт назначения - портовый город и получаем прямые морские ставки
        is_port_city = end_city.sea_terminals.exists()
        if is_port_city:
            end_terminals = end_city.sea_terminals.all()
            direct_sea_rates = SeaRate.objects.filter(
                sea_start_terminal=form.cleaned_data['sea_start_terminal'],
                sea_end_terminal__in=end_terminals
            ).annotate(truck=F('sea_end_terminal__local_hub_city__local_truck__price'))

        

    context = {
        'form': form,
        'direct_sea_rates': direct_sea_rates,
        'sea_truck': sea_truck,

        'line_rates': line_rates,
        'line_sea_rr_truck': line_sea_rr_truck,

        'agent_rates': agent_rates,
        'agent_sea_rr_truck': agent_sea_rr_truck

    }

    return render(request, 'paths/sea_rr_calculation.html', context)


@permission_required('paths.add_fileupload')
def file_upload(request):
        
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        SeaStartTerminal.objects.all().delete()
        SeaLine.objects.all().delete()
        SeaEndTerminal.objects.all().delete()
        SeaETD.objects.all().delete()
        LocalHubCity.objects.all().delete()

        POL = None

        if form.is_valid():
            uploaded_file = request.FILES['uploaded_file']
            all_sheets = pd.read_excel(uploaded_file, sheet_name=None)

            for sheet_name, df in all_sheets.items():

                if sheet_name == 'FOR':
                    sheet_errors = parse_for(df)
                    if sheet_errors:
                        for error in sheet_errors:
                            messages.error(request, error)
                    continue
                
                if sheet_name in ACCEPTABLE_POLS:
                    
                    for row in df.itertuples(index=False):

                        # Прежде всего проверяем, что цена есть хотя бы на один тип контейнера
                        rate_20 = get_container_prices(row[2])
                        rate_40 = get_container_prices(row[3])
                        if not rate_20 and not rate_40:
                            continue

                        # В первой колонке - порт отправки и дроп офф
                        first_col = row[0]
                        if isinstance(first_col, str):
                            POL, drop_off = get_pol(first_col)

                        # Во второй колонке - линия
                        second_col = row[1]
                        if isinstance(second_col, str):
                            sea_line = get_carrier(second_col)
                        
                        # В колонке E (пятая) - морские терминалы прибытия
                        POD_col = row[4]
                        if isinstance(POD_col, str):
                            pods = get_pods(POD_col)
                        
                        # В колонке F (седьмая) - ETD
                        year = datetime.date.today().year
                        etd_col = row[6]
                        etds = get_etd(etd_col, year)

                        # В десятой колонке - валидность
                        validity_col = row[9]
                        validity_date = make_dates([validity_col], year)[0]

                        # В колонке 12 - ставка конвертации
                        conversion_rate = get_conversion(row[11])

                        # В колонке 14 - агент или линия
                        agent = row[13]
                        is_agent = check_agent(agent)

                        for pod in pods:

                            sr = SeaRate(
                                sea_line=sea_line,
                                sea_start_terminal=POL,
                                validity=validity_date,
                                rate_20=rate_20,
                                rate_40=rate_40,
                                sea_end_terminal=pod,
                                conversion=conversion_rate,
                                agent=is_agent
                            )
                            sr.save()
                            if etds:
                                sr.etd.add(*etds)
                        
            messages.success(request, 'Файл успешно загружен!')

            # return redirect('paths:sea_rr_calculation')
    else:
        form = UploadForm()
    
    context = {'form': form}
    
    return render(request, 'paths/upload.html', context)