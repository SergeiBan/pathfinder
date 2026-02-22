from django.shortcuts import render, redirect
from .forms import SeaCalculationForm, ModalityForm, RRCalculationForm, SeaRRCalculationForm
from .models import SeaCalculation, SeaRate, InnerRRRate, SeaRRRate, LocalHubCity, SeaEndTerminal, RREndTerminal
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
    
    sea_to_rr = []
    if form.is_valid():
        print(form.cleaned_data['end_city'])
        
        if 'rr_end_terminal' in form.cleaned_data:
            end_terminals = RREndTerminal.objects.filter(pk=form.cleaned_data['rr_end_terminal'].pk)
        else:
            end_terminals = form.cleaned_data['end_city'].end_terminals.all()
        
        sea_rates = SeaRate.objects.filter(
            sea_start_terminal=form.cleaned_data['sea_start_terminal'],
            container=form.cleaned_data['container']
        ).distinct()
        rr_rates = InnerRRRate.objects.filter(
            end_terminal__in=end_terminals,
            container=form.cleaned_data['container']
        ).distinct().annotate(truck=F('end_terminal__city__local_truck__price'))

        city = form.cleaned_data['rr_end_terminal'].city
        is_port_city = city.sea_terminals.exists()
        if is_port_city:
            end_terminals = city.sea_terminals.all()
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
        'direct_sea_rates': direct_sea_rates
    }

    return render(request, 'paths/sea_rr_calculation.html', context)