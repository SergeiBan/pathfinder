from django.contrib import admin
from .models import (
    StartPort, SeaEndTerminal, SeaCalculation, SeaRRCalculation,
    SeaLine, SeaRate, SeaETD, LocalHubCity, StartPortCity,

    RRStartTerminal, RREndTerminal, RRETD, RRRate, InnerRRRate,
    RRStartCity, RREndCity,

    TruckEndCity
)


admin.site.register(LocalHubCity)
admin.site.register(StartPortCity)
admin.site.register(StartPort)
admin.site.register(SeaEndTerminal)
admin.site.register(SeaCalculation)
admin.site.register(SeaLine)
admin.site.register(SeaRate)
admin.site.register(SeaETD)

admin.site.register(RRStartTerminal)
admin.site.register(RREndTerminal)
admin.site.register(RRETD)
admin.site.register(RRRate)
admin.site.register(InnerRRRate)
admin.site.register(RRStartCity)
admin.site.register(RREndCity)

admin.site.register(SeaRRCalculation)

admin.site.register(TruckEndCity)
