from django.db import models
from django.db.models import Avg, Min
from . import constants, LocalHubCity, SeaStartTerminal

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


class InnerRRTerminal(models.Model):
    name = models.CharField('Внутренний ЖД терминал', max_length=64, unique=True)
    city = models.ForeignKey(LocalHubCity, verbose_name='Город ЖД терминала', on_delete=models.CASCADE, related_name='rr_terminals')
    gtd_20 = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    gtd_40 = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    vtt_20 = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    vtt_40 = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    local_truck = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Внутренний ЖД терминал'
        verbose_name_plural = 'Внутренние ЖД терминалы'

    def __str__(self):
        return self.name


class RRRate(models.Model):
    start_terminal = models.ForeignKey(ForeignRRStartTerminal, on_delete=models.CASCADE, related_name='direct_rr_rates')
    end_terminal = models.ForeignKey(InnerRRTerminal, on_delete=models.CASCADE, related_name='direct_rr_rates')
    etd = models.ManyToManyField(RRETD, related_name='direct_rr_rates')
    validity = models.DateField('Валидность до')
    container = models.CharField('Тип КТК', max_length=16, choices=constants.CONTAINER_OPTIONS)
    rate = models.DecimalField('Стоимость', max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.rate)
    
    class Meta:
        verbose_name = 'Прямая ЖД ставка'
        verbose_name_plural = 'Прямые ЖД ставки'


class InnerRRRate(models.Model):
    start_terminal = models.ForeignKey(InnerRRTerminal, verbose_name='ЖД терминал отправки', on_delete=models.CASCADE, related_name='inner_rates_outgoing')
    end_terminal = models.ForeignKey(InnerRRTerminal, verbose_name='ЖД терминал прибытия', on_delete=models.CASCADE, related_name='inner_rates_incoming')
    rate_20_24 = models.DecimalField('Стоимость за 20ft до 24т, $', max_digits=9, decimal_places=2, null=True, blank=True)
    rate_20_28 = models.DecimalField('Стоимость за 20ft 24-28т, $', max_digits=9, decimal_places=2, null=True, blank=True)
    rate_40 = models.DecimalField('Стоимость за 40ft, $', max_digits=9, decimal_places=2, null=True, blank=True)
    line = models.ForeignKey('SeaLine', verbose_name='Линия', on_delete=models.CASCADE, related_name='inner_rr_rates', null=True, blank=True)
    is_by_wagon = models.BooleanField('Повагонная отправка', default=False)
    thc = models.DecimalField('Терминальные расходы', max_digits=9, decimal_places=2)
    pol = models.ForeignKey(SeaStartTerminal, related_name='inner_rr_rates', null=True, blank=True, on_delete=models.CASCADE)

    def _check_for_line(self):
        if self.line:
            return {self.line}
        else:
            return False
    
    def check_for_truck(self):
        if self.end_terminal.city.local_truck:
            return f' Автовывоз по городу {self.end_terminal.city.local_truck}'
        return ''

    def __str__(self):
        line = self._check_for_line()
        truck = self.check_for_truck()
        if line:
             return f'{line}. {self.start_terminal} - {self.end_terminal}{truck}'
        return f'{self.start_terminal} - {self.end_terminal}{truck}'
    
    class Meta:
        verbose_name = 'Внутренняя ЖД ставка'
        verbose_name_plural = 'Внутренние ЖД ставки'
    

    def get_price(self, container, gross, is_vtt):
        price = None
        if self.container == '20DC':
            if gross <= 24000:
                price = self.rate_20_24
            else:
                price = self.rate_20_28
        else:
            price = self.rate_40
        
        return f'{price} ₽'