from django.db import models
from django.db.models import Avg, Min
from . import constants
from . import StartPort, SeaEndTerminal


class TruckEndCity(models.Model):
    name = models.CharField('Город автодовоза', max_length=32, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Город автодовоза'
        verbose_name_plural = 'Города автодовоза'
