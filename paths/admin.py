from django.contrib import admin
from .models import (
    StartPort, SeaEndTerminal, SeaCalculation,
    SeaLine, SeaRate
)


admin.site.register(StartPort)
admin.site.register(SeaEndTerminal)
admin.site.register(SeaCalculation)
admin.site.register(SeaLine)
admin.site.register(SeaRate)
