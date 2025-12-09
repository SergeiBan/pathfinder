from django.shortcuts import render
from .forms import CalculationForm
from .models import Calculation


def index(request):
    form = CalculationForm(request.POST or None)
    context = {
        'form': form
    }

    if form.is_valid():
        form = form.save()

    return render(request, 'paths/index.html', context)
