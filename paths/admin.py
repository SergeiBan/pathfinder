from django.contrib import admin
from .models import (
    StartPort, SeaEndTerminal, SeaCalculation,
    SeaLine, SeaRate, SeaETD,

    RRStartTerminal, RREndTerminal, RRETD, RRRate,
    RRStartCity, RREndCity
)


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
admin.site.register(RRStartCity)
admin.site.register(RREndCity)
