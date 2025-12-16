from django.shortcuts import render
from .forms import SeaCalculationForm
from .models import SeaCalculation


def index(request):
    form = SeaCalculationForm(request.POST or None)

    if form.is_valid():
        form.save()

    context = {
        'form': form
    }

    return render(request, 'paths/index.html', context)
