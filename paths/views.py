from django.shortcuts import render
from .forms import StartCityForm
from .models import StartCity


def index(request):
    form = StartCityForm(request.GET or None)
    context = {
        'form': form,
    }
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