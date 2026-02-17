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




class ForeignRRStartCity(models.Model):
    name = models.CharField('Зарубежный город ЖД отправки', max_length=32, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Зарубежный город ЖД отправки'
        verbose_name_plural = 'Зарубежные города ЖД отправки'



class ForeignRRStartTerminal(models.Model):
    name = models.CharField('Зарубежный ЖД терминал отправки', max_length=32, unique=True)
    city = models.ForeignKey(ForeignRRStartCity, verbose_name='Город ЖД отправки', on_delete=models.CASCADE, related_name='start_terminals')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'ЖД терминал отправки'
        verbose_name_plural = 'ЖД терминалы отправки'


class InnerRRStartTerminal(models.Model):
    name = models.CharField('Внутренний ЖД терминал отправки', max_length=32, unique=True)
    city = models.ForeignKey(LocalHubCity, verbose_name='Город ЖД отправки', on_delete=models.CASCADE, related_name='start_terminals')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Внутренний ЖД терминал отправки'
        verbose_name_plural = 'Внутренние ЖД терминалы отправки'



class RREndTerminal(models.Model):
    name = models.CharField('ЖД терминал прибытия', max_length=32, unique=True)
    city = models.ForeignKey(LocalHubCity, verbose_name='Город ЖД прибытия', on_delete=models.CASCADE, related_name='end_terminals')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'ЖД терминал прибытия'
        verbose_name_plural = 'ЖД терминалы прибытия'


class RRRate(models.Model):
    start_terminal = models.ForeignKey(ForeignRRStartTerminal, on_delete=models.CASCADE, related_name='rates')
    end_terminal = models.ForeignKey(RREndTerminal, on_delete=models.CASCADE, related_name='rates')
    etd = models.ManyToManyField(RRETD, related_name='rates')
    validity = models.DateField('Валидность до')
    container = models.CharField('Тип КТК', max_length=16, choices=constants.CONTAINER_OPTIONS)
    rate = models.DecimalField('Стоимость', max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.rate)
    
    class Meta:
        verbose_name = 'Прямая ЖД ставка'
        verbose_name_plural = 'Прямые ЖД ставки'


class InnerRRRate(models.Model):
    start_terminal = models.ForeignKey(InnerRRStartTerminal, on_delete=models.CASCADE, related_name='inner_rates')
    end_terminal = models.ForeignKey(RREndTerminal, on_delete=models.CASCADE, related_name='inner_rates')
    container = models.CharField('Тип КТК', max_length=16, choices=constants.CONTAINER_OPTIONS)
    rate = models.DecimalField('Стоимость', max_digits=9, decimal_places=2)

    def __str__(self):
        return f'{self.rate} {self.start_terminal} - {self.end_terminal}'
    
    class Meta:
        verbose_name = 'Внутренняя ЖД ставка'
        verbose_name_plural = 'Внутренние ЖД ставки'