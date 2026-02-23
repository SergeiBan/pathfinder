from django.shortcuts import render, redirect
from .forms import SeaCalculationForm, ModalityForm, RRCalculationForm, SeaRRCalculationForm
from .models import (
    SeaCalculation, SeaRate, InnerRRRate, LocalHubCity, SeaEndTerminal, InnerRRTerminal,
    DistantTruckRate
)
from .utils import find_seapath, find_all_seapaths
from django.db.models import F


def index(request):
    form = ModalityForm(request.GET or None)

    if form.is_valid():
        print(form.cleaned_data)
        if form.cleaned_data['modality'] == 'sea':
            return redirect('paths:sea_calculation')
        elif form.cleaned_data['modality'] == 'rr':
            return redirect('paths:rr_calculation')
        elif form.cleaned_data['modality'] == 'sea_rr':
            return redirect('paths:sea_rr_calculation')

    context = {
        'form': form
    }

    return render(request, 'paths/index.html', context)


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
        'sea_rr_truck': sea_rr_truck
    }

    return render(request, 'paths/sea_rr_calculation.html', context)