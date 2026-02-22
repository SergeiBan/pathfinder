from django.db import models
from django.db.models import Avg, Min
from . import (
    SeaEndTerminal, SeaStartTerminal, SeaRate, ForeignRRStartCity,
    RRETD, RRRate, ForeignRRStartTerminal, RREndTerminal, LocalHubCity
)
from datetime import date


CONTAINER_OPTIONS = (
    ('20DC', '20DC'),
    ('H0HC', '40HC'),
)


class SeaCalculation(models.Model):
    sea_start_terminal = models.ForeignKey(SeaStartTerminal, verbose_name='Терминал отправки', on_delete=models.CASCADE, related_name='sea_calculations')
    sea_end_terminal = models.ForeignKey(SeaEndTerminal, verbose_name='Терминал прибытия', on_delete=models.CASCADE, related_name='sea_calculations')
    etd_from = models.DateField('Выход от', blank=True, null=True)
    etd_to = models.DateField('Выход до', blank=True, null=True)
    container = models.CharField('Тип КТК', max_length=16, choices=CONTAINER_OPTIONS)
    cheapest = models.ForeignKey(SeaRate, on_delete=models.CASCADE, related_name='cheapest_calculations')
    fastest = models.ForeignKey(SeaRate, on_delete=models.CASCADE, related_name='fastest_calculations')

    def save(self, *args, **kwargs):
        applicable_rates = SeaRate.objects.filter(start_port=self.start_port, sea_end_terminal=self.sea_end_terminal, container=self.container)
        if applicable_rates:
            today = date.today()

            if self.etd_from is None and self.etd_to is None:
                applicable_rates = applicable_rates.filter(etd__etd__gt=today)

                if applicable_rates:
                    self.cheapest= applicable_rates.order_by('rate').first()
                    self.fastest = applicable_rates.order_by('etd__etd').first()
                    super().save(*args, **kwargs)
            
            elif self.etd_from is None and self.etd_to is not None:
                applicable_rates = applicable_rates.filter(etd__etd__gt=today, etd__etd__lte=self.etd_to)

                if applicable_rates:
                    self.cheapest= applicable_rates.order_by('rate').first()
                    self.fastest = applicable_rates.order_by('etd__etd').first()
                    super().save(*args, **kwargs)

            elif self.etd_from is not None and self.etd_to is None:
                applicable_rates = applicable_rates.filter(etd__etd__gte=self.etd_from)

                if applicable_rates:
                    self.cheapest= applicable_rates.order_by('rate').first()
                    self.fastest = applicable_rates.order_by('etd__etd').first()
                    super().save(*args, **kwargs)
            
            elif self.etd_from is not None and self.etd_to is not None:
                applicable_rates = applicable_rates.filter(etd__etd__gte=self.etd_from, etd__etd__lte=self.etd_to)
                if applicable_rates:
                    self.cheapest= applicable_rates.order_by('rate').first()
                    self.fastest = applicable_rates.order_by('etd__etd').first()
                    super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Расчёт моря"
        verbose_name_plural = "Расчёты моря"



class RRCalculation(models.Model):
    start_city = models.ForeignKey(ForeignRRStartCity, on_delete=models.CASCADE, related_name='rr_calculations')
    end_city = models.ForeignKey(LocalHubCity, on_delete=models.CASCADE, related_name='rr_calculations')
    etd_from = models.DateField('Выход от', blank=True, null=True)
    etd_to = models.DateField('Выход до', blank=True, null=True)
    container = models.CharField('Тип КТК', max_length=16, choices=CONTAINER_OPTIONS)
    cheapest = models.ForeignKey(RRRate, on_delete=models.CASCADE, related_name='cheapest_calculations')
    fastest = models.ForeignKey(RRRate, on_delete=models.CASCADE, related_name='fastest_calculations')

    def save(self, *args, **kwargs):
        relevant_start_terminals = ForeignRRStartTerminal.objects.filter(city=self.start_city)
        relevant_end_terminals = RREndTerminal.objects.filter(city=self.end_city)
        applicable_rates = RRRate.objects.filter(
            start_terminal__in=relevant_start_terminals,
            end_terminal__in=relevant_end_terminals,
            container=self.container)
        if applicable_rates:
            today = date.today()

            if self.etd_from is None and self.etd_to is None:
                applicable_rates = applicable_rates.filter(etd__etd__gt=today)

                if applicable_rates:
                    self.cheapest= applicable_rates.order_by('rate').first()
                    self.fastest = applicable_rates.order_by('etd__etd').first()
                    super().save(*args, **kwargs)
            
            elif self.etd_from is None and self.etd_to is not None:
                applicable_rates = applicable_rates.filter(etd__etd__gt=today, etd__etd__lte=self.etd_to)

                if applicable_rates:
                    self.cheapest= applicable_rates.order_by('rate').first()
                    self.fastest = applicable_rates.order_by('etd__etd').first()
                    super().save(*args, **kwargs)

            elif self.etd_from is not None and self.etd_to is None:
                applicable_rates = applicable_rates.filter(etd__etd__gte=self.etd_from)

                if applicable_rates:
                    self.cheapest= applicable_rates.order_by('rate').first()
                    self.fastest = applicable_rates.order_by('etd__etd').first()
                    super().save(*args, **kwargs)
            
            elif self.etd_from is not None and self.etd_to is not None:
                applicable_rates = applicable_rates.filter(etd__etd__gte=self.etd_from, etd__etd__lte=self.etd_to)
                if applicable_rates:
                    self.cheapest= applicable_rates.order_by('rate').first()
                    self.fastest = applicable_rates.order_by('etd__etd').first()
                    super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Расчёт прямого ЖД"
        verbose_name_plural = "Расчёты прямого ЖД"



class SeaRRCalculation(models.Model):
    sea_start_terminal = models.ForeignKey(SeaStartTerminal, verbose_name='Морской терминал отправки', on_delete=models.CASCADE, related_name='calculations')
    rr_end_terminal = models.ForeignKey(RREndTerminal, verbose_name='ЖД терминал прибытия', on_delete=models.CASCADE, related_name='calculations')
    end_city = models.ForeignKey(LocalHubCity, on_delete=models.CASCADE, related_name='calculations')
    etd_from = models.DateField('Выход от', blank=True, null=True)
    etd_to = models.DateField('Выход до', blank=True, null=True)
    container = models.CharField('Тип КТК', max_length=16, choices=CONTAINER_OPTIONS)
    gross = models.DecimalField('Брутто', max_digits=20, decimal_places=10)
    is_VTT = models.BooleanField('ВТТ', default=False)