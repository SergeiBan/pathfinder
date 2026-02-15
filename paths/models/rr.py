from django.db import models
from django.db.models import Avg, Min
from . import constants, LocalHubCity

class RRETD(models.Model):
    etd = models.DateField('Дата выхода ЖД')

    def __str__(self):
        return str(self.etd)

    class Meta:
        ordering = ['etd']
        verbose_name = 'Дата выхода ЖД'
        verbose_name_plural = 'Даты выхода ЖД'




class RRStartCity(models.Model):
    name = models.CharField('Город ЖД отправки', max_length=32, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Город ЖД отправки'
        verbose_name_plural = 'Города ЖД отправки'


class RREndCity(models.Model):
    name = models.CharField('Город ЖД прибытия', max_length=32, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Город ЖД прибытия'
        verbose_name_plural = 'Города ЖД прибытия'



class RRStartTerminal(models.Model):
    name = models.CharField('ЖД терминал отправки', max_length=32, unique=True)
    city = models.ForeignKey(RRStartCity, verbose_name='Город ЖД отправки', on_delete=models.CASCADE, related_name='start_terminals')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'ЖД терминал отправки'
        verbose_name_plural = 'ЖД терминалы отправки'



class RREndTerminal(models.Model):
    name = models.CharField('ЖД терминал прибытия', max_length=32, unique=True)
    city = models.ForeignKey(RREndCity, verbose_name='Город ЖД прибытия', on_delete=models.CASCADE, related_name='end_terminals')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'ЖД терминал прибытия'
        verbose_name_plural = 'ЖД терминалы прибытия'


class RRRate(models.Model):
    start_terminal = models.ForeignKey(RRStartTerminal, on_delete=models.CASCADE, related_name='rates')
    end_terminal = models.ForeignKey(RREndTerminal, on_delete=models.CASCADE, related_name='rates')
    etd = models.ManyToManyField(RRETD, related_name='rates')
    validity = models.DateField('Валидность до')
    container = models.CharField('Тип КТК', max_length=16, choices=constants.CONTAINER_OPTIONS)
    rate = models.DecimalField('Стоимость', max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.rate)
    
    class Meta:
        verbose_name = 'ЖД ставка'
        verbose_name_plural = 'ЖД ставки'


class InnerRRRate(models.Model):
    start_terminal = models.ForeignKey(RRStartTerminal, on_delete=models.CASCADE, related_name='inner_rates')
    end_terminal = models.ForeignKey(RREndTerminal, on_delete=models.CASCADE, related_name='inner_rates')
    container = models.CharField('Тип КТК', max_length=16, choices=constants.CONTAINER_OPTIONS)
    rate = models.DecimalField('Стоимость', max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.rate)
    
    class Meta:
        verbose_name = 'Внутренняя ЖД ставка'
        verbose_name_plural = 'Внутренние ЖД ставки'