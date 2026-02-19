from django.db import models
from django.db.models import Avg, Min
from . import constants
from . import SeaStartTerminal, SeaEndTerminal, LocalHubCity, SeaRate, InnerRRRate


class EndCity(models.Model):
    name = models.CharField('Город назначения', max_length=32, unique=True)
    rate = models.DecimalField('Стоимость автовывоза', max_digits=9, decimal_places=2)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Город назначения'
        verbose_name_plural = 'Города назначения'


class TruckToEndCityRate(models.Model):
    local_hub_cities = models.ManyToManyField(LocalHubCity, related_name='end_city_rates')
    end_cities = models.ManyToManyField(EndCity, related_name='end_city_rates')
    price = models.DecimalField('Цена автовывоза до конечного города', max_digits=9, decimal_places=2)


class SeaRRRate(models.Model):
    sea_rate = models.ForeignKey(SeaRate, on_delete=models.CASCADE, related_name='sea_rr_rates')
    inner_rr_rate = models.ForeignKey(InnerRRRate, on_delete=models.CASCADE, related_name='sea_rr_rates', null=True, blank=True)

    def __str__(self):
        return f'{self.sea_rate} + {self.inner_rr_rate}'
    
    class Meta:
        verbose_name = 'Ставка море + ЖД'
        verbose_name_plural = 'Ставки море + ЖД'