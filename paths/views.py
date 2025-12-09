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


def search_start(request):
    if request.htmx:
        search = request.POST['search']
        start_cities = None
        if search:
            start_cities = StartCity.objects.filter(name__startswith=search)
    context = {
        'start_cities': start_cities
    }
    print(start_cities or None)
    return render(request, 'paths/found_start_city.html', context)