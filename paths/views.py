from django.shortcuts import render, redirect
from .forms import SeaCalculationForm, ModalityForm
from .models import SeaCalculation


def index(request):
    form = ModalityForm(request.GET or None)

    if form.is_valid():
        print(form.cleaned_data)
        if form.cleaned_data['modality'] == 'sea':
            return redirect('paths:sea_calculation')

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
