from django.shortcuts import render, redirect
from .forms import SeaCalculationForm, RRCalculationForm, SeaRRCalculationForm, UploadForm
from .models import (
    SeaCalculation, SeaRate, InnerRRRate, LocalHubCity, SeaEndTerminal, InnerRRTerminal,
    DistantTruckRate
)
from .utils import find_seapath, find_all_seapaths
from django.db.models import F
from django.http import Http404
from django.contrib.auth.decorators import permission_required
import pandas as pd


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
    sea_rr_rates = None
    direct_sea_rates = None
    end_terminals = None
    remote_truck_rates = None
    sea_rr_truck = []
    sea_truck = []
    
    sea_to_rr = []
    if form.is_valid():
        end_city = form.cleaned_data['end_city']
        particular_rr_terminal = form.cleaned_data['rr_end_terminal']

        
        # Если выбран конкретный ЖД терминал прибытия
        if particular_rr_terminal:
            end_terminals = InnerRRTerminal.objects.filter(pk=form.cleaned_data['rr_end_terminal'].pk)
        else:
            end_terminals = end_city.rr_terminals.all()
        
        # Получаем все морские ставки из терминала отправления во все российские терминалы
        sea_rates = SeaRate.objects.filter(
            sea_start_terminal=form.cleaned_data['sea_start_terminal'],
            container=form.cleaned_data['container']
        ).distinct()

        agent_rates = sea_rate.filter(agent__isnull=True)
        line_rates = sea_rate.filter(agent__isnull=False)

        # Получаем все ЖД ставки из всех морских терминалов прибытия во все ЖД терминалы города доставки
        rr_rates = InnerRRRate.objects.filter(
            end_terminal__in=end_terminals,
            container=form.cleaned_data['container']
        ).distinct().annotate(truck=F('end_terminal__city__local_truck__price'))


        # Если нужен автовывоз в другой город
        if end_city.ingoing_truck_rates.exists():
            remote_truck_rates = end_city.ingoing_truck_rates.all()
            all_rr_rates = InnerRRRate.objects.all()

            # Сопоставляем ставки ЖД и автовывоза по городу
            rr_plus_truck_rates = []
            for remote_truck in remote_truck_rates:
                for rr_rate in all_rr_rates:
                    if rr_rate.end_terminal.city == remote_truck.start_city:
                        rr_plus_truck_rates.append([rr_rate, remote_truck])

            # Сопоставляем морские ставки и ЖД ставки по городу
            sea_rr_truck = []
            for sea_rate in sea_rates:
                for rr_truck in rr_plus_truck_rates:
                    if sea_rate.sea_end_terminal.local_hub_city == rr_truck[0].start_terminal.city:
                        sea_rr_truck.append([sea_rate, rr_truck[0], rr_truck[1]])
            
            # Сопоставляем морские ставки и ставки автовывоза по городу
            for sea_rate in sea_rates:
                for truck_rate in remote_truck_rates:
                    if sea_rate.sea_end_terminal.local_hub_city == truck_rate.start_city:
                        sea_truck.append([sea_rate, truck_rate])

        # Проверям, что пункт назначения - портовый город и получаем прямые морские ставки
        is_port_city = end_city.sea_terminals.exists()
        if is_port_city:
            end_terminals = end_city.sea_terminals.all()
            direct_sea_rates = SeaRate.objects.filter(
                sea_start_terminal=form.cleaned_data['sea_start_terminal'],
                sea_end_terminal__in=end_terminals
            ).annotate(truck=F('sea_end_terminal__local_hub_city__local_truck__price'))

        # Мультимодальная ставка составляется из морской и ЖД ставок
        for sea_rate in sea_rates:
            for rr_rate in rr_rates:
                if sea_rate.sea_end_terminal.local_hub_city == rr_rate.start_terminal.city:
                    sea_to_rr.append([sea_rate, rr_rate])


    context = {
        'form': form,
        'rates': sea_to_rr,
        'direct_sea_rates': direct_sea_rates,
        'sea_rr_truck': sea_rr_truck,
        'sea_truck': sea_truck
    }

    return render(request, 'paths/sea_rr_calculation.html', context)


@permission_required('paths.add_fileupload')
def file_upload(request):
        
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['uploaded_file']
            all_sheets = pd.read_excel(uploaded_file, sheet_name=None)

            pols_to_create = []
            for sheet_name, df in all_sheets.items():
                
                if sheet_name == 'Shanghai':
                    
                    for row in df.itertuples(index=False):
                        first_col = row[0]
                        if isinstance(first_col, str) and 'POL:' in first_col:
                            sea_start = first_col[4:].split('\n')

                            POL = sea_start[0]
                            if len(sea_start) > 2:
                                drop_off = ' '.join(sea_start[1:])
                            else:
                                drop_off = sea_start[1]
                            # pols_to_create.append()


            return redirect('paths:sea_rr_calculation')
    else:
        form = UploadForm()
    
    context = {'form': form}
    
    return render(request, 'paths/upload.html', context)