from django.contrib import admin
from .models import (
    StartPort, EndPort, RRHub, RRStation, Calculation,
    SeaLine, SeaRate, EndPortSatellite, InlandEndCity
)


admin.site.register(StartPort)
admin.site.register(EndPort)
admin.site.register(RRHub)
admin.site.register(RRStation)
admin.site.register(Calculation)
admin.site.register(SeaLine)
admin.site.register(SeaRate)
admin.site.register(EndPortSatellite)
admin.site.register(InlandEndCity)