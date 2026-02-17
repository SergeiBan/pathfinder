from django.contrib import admin
from .models import (
    SeaStartTerminal, SeaEndTerminal, SeaCalculation, SeaRRCalculation,
    SeaLine, SeaRate, SeaETD, LocalHubCity,

    ForeignRRStartTerminal, RREndTerminal, RRETD, RRRate, InnerRRRate,
    ForeignRRStartCity, InnerRRStartTerminal, SeaRRRate,

    EndCity
)


admin.site.register(LocalHubCity)
admin.site.register(SeaStartTerminal)
admin.site.register(SeaEndTerminal)
admin.site.register(SeaCalculation)
admin.site.register(SeaLine)
admin.site.register(SeaRate)
admin.site.register(SeaETD)

admin.site.register(ForeignRRStartTerminal)
admin.site.register(InnerRRStartTerminal)
admin.site.register(RREndTerminal)
admin.site.register(RRETD)
admin.site.register(RRRate)
admin.site.register(InnerRRRate)
admin.site.register(ForeignRRStartCity)

admin.site.register(SeaRRCalculation)
admin.site.register(SeaRRRate)


admin.site.register(EndCity)


