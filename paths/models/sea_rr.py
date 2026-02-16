from django.db import models
from django.db.models import Avg, Min
from . import constants
from . import SeaStartTerminal, SeaEndTerminal


class EndCity(models.Model):
    name = models.CharField('Город назначения', max_length=32, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Город назначения'
        verbose_name_plural = 'Города назначения'
