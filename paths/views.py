from django.shortcuts import render, redirect
from .forms import SeaCalculationForm, ModalityForm, RRCalculationForm, SeaRRCalculationForm
from .models import SeaCalculation, SeaRate, InnerRRRate
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

    if form.is_valid():
        # form.save()
        
        if 'rr_end_city' in form.cleaned_data:
            pass
        sea_rates = find_all_seapaths(
            form.cleaned_data['sea_start_terminal'],
            form.cleaned_data['container'],
            SeaRate,
            form.cleaned_data['etd_from'],
            form.cleaned_data['etd_to']
        )
        print(sea_rates)
        # find_inner_rrpath(sea_rates, InnerRRRate, rr_end_terminal=form.cleaned_data['rr_end_terminal'])
        # print(form.cleaned_data)

    context = {
        'form': form
    }

    return render(request, 'paths/sea_rr_calculation.html', context)