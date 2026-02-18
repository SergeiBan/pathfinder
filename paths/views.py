from django.shortcuts import render, redirect
from .forms import SeaCalculationForm, ModalityForm, RRCalculationForm, SeaRRCalculationForm
from .models import SeaCalculation, SeaRate, InnerRRRate, SeaRRRate, LocalHubCity, SeaEndTerminal
from .utils import find_seapath, find_all_seapaths


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
    if form.is_valid():
        # form.save()
        
        if 'rr_end_city' in form.cleaned_data:
            pass

        elif 'rr_end_terminal' in form.cleaned_data:
            sea_rr_rates = SeaRRRate.objects.filter(
                sea_rate__sea_start_terminal=form.cleaned_data['sea_start_terminal'],
                sea_rate__container=form.cleaned_data['container'],
                inner_rr_rate__end_terminal=form.cleaned_data['rr_end_terminal'],
                inner_rr_rate__container=form.cleaned_data['container'],
            )
        
        sea_rates = SeaRate.objects.filter(
            sea_start_terminal=form.cleaned_data['sea_start_terminal'],
            container=form.cleaned_data['container']
        ).distinct()
        rr_rates = InnerRRRate.objects.filter(
            end_terminal=form.cleaned_data['rr_end_terminal'],
            container=form.cleaned_data['container']
        ).distinct()

        is_port_city = form.cleaned_data['rr_end_terminal'].city.sea_terminals.exists()
        sea_to_rr = []
        for sea_rate in sea_rates:
            for rr_rate in rr_rates:
                if sea_rate.sea_end_terminal.local_hub_city == rr_rate.start_terminal.city:
                    sea_to_rr.append([sea_rate, rr_rate])
        print(is_port_city)
        

    context = {
        'form': form,
        'rates': sea_rr_rates
    }

    return render(request, 'paths/sea_rr_calculation.html', context)