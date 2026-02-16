from django.contrib import admin
from .models import (
    SeaStartTerminal, SeaEndTerminal, SeaCalculation, SeaRRCalculation,
    SeaLine, SeaRate, SeaETD, LocalHubCity,

    RRStartTerminal, RREndTerminal, RRETD, RRRate, InnerRRRate,
    RRStartCity, RREndCity,

    EndCity
)


admin.site.register(LocalHubCity)
admin.site.register(SeaStartTerminal)
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

admin.site.register(EndCity)
