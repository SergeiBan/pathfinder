from django.shortcuts import render, redirect
from .forms import SeaCalculationForm, ModalityForm, RRCalculationForm, SeaRRCalculationForm
from .models import SeaCalculation


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
        print('valid')

    context = {
        'form': form
    }

    return render(request, 'paths/sea_rr_calculation.html', context)