from django.db import models
from django.db.models import Avg, Min
from . import constants
from . import SeaStartTerminal, SeaEndTerminal, LocalHubCity, SeaRate, InnerRRRate


class SeaRRRate(models.Model):
    sea_rate = models.ForeignKey(SeaRate, on_delete=models.CASCADE, related_name='sea_rr_rates')
    inner_rr_rate = models.ForeignKey(InnerRRRate, on_delete=models.CASCADE, related_name='sea_rr_rates', null=True, blank=True)

    def __str__(self):
        return f'{self.sea_rate} + {self.inner_rr_rate}'
    
    class Meta:
        verbose_name = 'Ставка море + ЖД'
        verbose_name_plural = 'Ставки море + ЖД'