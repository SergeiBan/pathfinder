from django.db import models
from django.db.models import Avg, Min
from . import SeaEndTerminal, StartPort, SeaRate

CONTAINER_OPTIONS = (
    ('20DC', '20DC'),
    ('H0HC', '40HC'),
)


class SeaCalculation(models.Model):
    start_port = models.ForeignKey(StartPort, verbose_name='Порт отправки', on_delete=models.CASCADE, related_name='sea_calculations')
    sea_end_terminal = models.ForeignKey(SeaEndTerminal, verbose_name='Терминал прибытия', on_delete=models.CASCADE, related_name='sea_calculations')
    etd = models.DateField('Дата выхода')
    container = models.CharField('Тип КТК', max_length=16, choices=CONTAINER_OPTIONS)
    cheapest = models.ForeignKey(SeaRate, on_delete=models.CASCADE, related_name='cheapest_calculations')
    fastest = models.ForeignKey(SeaRate, on_delete=models.CASCADE, related_name='fastest_calculations')

    def save(self, *args, **kwargs):
        applicable_rates = SeaRate.objects.filter(start_port=self.start_port, sea_end_terminal=self.sea_end_terminal, etd__lte=self.etd, container=self.container)
        if applicable_rates:
            print(applicable_rates)
            self.cheapest= applicable_rates.order_by('rate').first()
            self.fastest = applicable_rates.order_by('etd').first()
            super().save(*args, **kwargs)
   