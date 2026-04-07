from django.shortcuts import render, redirect
from .forms import SeaCalculationForm, RRCalculationForm, SeaRRCalculationForm, UploadForm
from .models import (
    SeaCalculation, SeaRate, InnerRRRate, LocalHubCity, SeaEndTerminal, InnerRRTerminal,
    DistantTruckRate, SeaStartTerminal, SeaLine, SeaETD, ACCEPTABLE_POLS, ACCEPTABLE_AGENTS,
    ForeignAgent
)
from .utils import (
    get_line_mm_rates, get_agent_mm_rates, find_seapath, find_all_seapaths, get_pol,
    get_carrier, get_pods, get_etd, get_container_prices, make_dates, get_conversion,
    check_agent
)
from django.db.models import F, QuerySet
from django.http import Http404
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
import pandas as pd
import datetime

from .parse_rr import parse_for
from .parse_trucks import parse_truck_sheet
from .parse_sea import parse_sea_sheet


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
    container = None
    is_vtt = False
    gross = None
    
    if form.is_valid():
        end_city = form.cleaned_data['end_city']
        particular_rr_terminal = form.cleaned_data['rr_end_terminal']
        gross = form.cleaned_data['gross']
        container = form.cleaned_data['container']
        is_vtt = form.cleaned_data['is_VTT']
        
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
            line_sea_rates, InnerRRRate, end_terminals, form.cleaned_data['container'], end_city, gross)
        
        agent_rates, agent_sea_rr_truck = get_agent_mm_rates(
            agent_sea_rates, InnerRRRate, end_terminals, form.cleaned_data['container'], end_city, gross)

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
            ).annotate(truck=F('sea_end_terminal__local_hub_city__local_truck'))

    context = {
        'form': form,
        'direct_sea_rates': direct_sea_rates,
        'sea_truck': sea_truck,

        'line_rates': line_rates,
        'line_sea_rr_truck': line_sea_rr_truck,

        'agent_rates': agent_rates,
        'agent_sea_rr_truck': agent_sea_rr_truck,
        'gross': gross,
        'container': container,
        'is_vtt': is_vtt
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
        SeaRate.objects.all().delete()
        InnerRRRate.objects.all().delete()
        ForeignAgent.objects.all().delete()

        POL = None

        if form.is_valid():
            uploaded_file = request.FILES['uploaded_file']
            all_sheets = pd.read_excel(uploaded_file, sheet_name=None)
            sheet_errors = []

            for sheet_name, df in all_sheets.items():
                
                if sheet_name.upper() in ACCEPTABLE_POLS:
                    sheet_errors.append(parse_sea_sheet(sheet_name, df))
                
                if sheet_name == 'FOR':
                    sheet_errors.append(parse_for(df))
                    continue

                if sheet_name == 'Автовывоз':
                    sheet_errors.append(parse_truck_sheet(df))
                    continue
            
            if sheet_errors:
                for error in sheet_errors:
                    messages.error(request, error)
                        
            else:
                messages.success(request, 'Файл успешно загружен!')

    else:
        form = UploadForm()
    
    context = {'form': form}
    
    return render(request, 'paths/upload.html', context)