from django.contrib import admin
from .models import (
    SeaStartTerminal, SeaEndTerminal, SeaCalculation, SeaRRCalculation,
    SeaLine, SeaRate, SeaETD, LocalHubCity, DistantTruckRate,
    ForeignAgent,

    ForeignRRStartTerminal, InnerRRTerminal, RRETD, RRRate, InnerRRRate,
    ForeignRRStartCity,

)


class SeaRateAdmin(admin.ModelAdmin):
    list_display = ('sea_line', 'sea_start_terminal', 'sea_end_terminal', 'agent')
    list_filter = ('sea_line', 'sea_start_terminal', 'sea_end_terminal', 'agent')


admin.site.register(LocalHubCity)
admin.site.register(DistantTruckRate)

admin.site.register(SeaStartTerminal)
admin.site.register(SeaEndTerminal)
admin.site.register(SeaCalculation)
admin.site.register(SeaLine)
admin.site.register(SeaRate, SeaRateAdmin)
admin.site.register(SeaETD)
admin.site.register(ForeignAgent)

admin.site.register(ForeignRRStartTerminal)
admin.site.register(InnerRRTerminal)
admin.site.register(RRETD)
admin.site.register(RRRate)
admin.site.register(InnerRRRate)
admin.site.register(ForeignRRStartCity)

admin.site.register(SeaRRCalculation)



