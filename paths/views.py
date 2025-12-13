from django.shortcuts import render
from .forms import SeaCalculationForm
from .models import SeaCalculation


def index(request):
    form = SeaCalculationForm(request.POST or None)
    context = {
        'form': form
    }

    if form.is_valid():
        form = form.save()

    return render(request, 'paths/index.html', context)
