from django.contrib import admin
from .models import StartCity, EndCity, RRHub, RRStation, Calculation


admin.site.register(StartCity)
admin.site.register(EndCity)
admin.site.register(RRHub)
admin.site.register(RRStation)
admin.site.register(Calculation)