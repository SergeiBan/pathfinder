from django.contrib import admin
from .models import (
    ForeignPort, EndCity, RRHub, RRStation, Calculation,
    SeaLine, SeaRate
)


admin.site.register(ForeignPort)
admin.site.register(EndCity)
admin.site.register(RRHub)
admin.site.register(RRStation)
admin.site.register(Calculation)
admin.site.register(SeaLine)
admin.site.register(SeaRate)
