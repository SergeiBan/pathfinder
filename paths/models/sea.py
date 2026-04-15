from django.db import models
from django.db.models import Avg, Min
from . import constants


FOREIGN_PORTS = (
    ('Shanghai', 'Shanghai'),
    ('Ningbo', 'Ningbo'),
    ('Tianjin', 'Tianjin'), 
    ('Dalian', 'Dalian'),
    ('Qingdao', 'Qingdao'),
    ('Rizhao', 'Rizhao'),
    ('Xiamen', 'Xiamen'),
    ('Nansha', 'Nansha'),
    ('Guangzhou', 'Guangzhou'),
    ('Yantian', 'Yantian'),
    ('Shekou', 'Shekou'),
    ('Lianyungang', 'Lianyungang'),
    ('Hongkong', 'Hongkong'),
    ('Taicang', 'Taicang'),
)


class SeaStartTerminal(models.Model):
    name = models.CharField('Порт отправки', max_length=32, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Порт отправки'
        verbose_name_plural = 'Порты отправки'
        ordering = ('name',)

class LocalHubCity(models.Model):
    name = models.CharField('Внутренний транспортный хаб', max_length=32, unique=True)
    local_truck = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Внутренний транспортный хаб'
        verbose_name_plural = 'Внутренние транспортные хабы'
        ordering = ('name',)

    def __str__(self):
            return self.name
    
    def save(self, *args, **kwargs):
        if self.name in ['МОСКВА', 'САНКТ-ПЕТЕРБУРГ']:
            self.local_truck = 25000
        elif self.name in ['НОВОСИБИРСК', 'ЕКАТЕРИНБУРГ']:
            self.local_truck = 20000

        super().save(*args, **kwargs)


class DistantTruckRate(models.Model):
    start_city = models.ForeignKey(LocalHubCity, on_delete=models.CASCADE, related_name='outgoing_truck_rates', verbose_name='Город отправки автовывоза')
    end_city = models.ForeignKey(LocalHubCity, on_delete=models.CASCADE, related_name='ingoing_truck_rates', verbose_name='Город прибытия автовывоза')
    price = models.DecimalField('Цена автовывоза между городами', max_digits=9, decimal_places=2)

    def __str__(self):
        return f'автовывоз {self.price} ₽: {self.start_city} - {self.end_city}'
    
    class Meta:
        verbose_name = 'Автовывоз между городами'
        verbose_name_plural = 'Автовывозы между городами'


class SeaEndTerminal(models.Model):
    name = models.CharField('Морской терминал прибытия', max_length=32, unique=True)
    local_hub_city = models.ForeignKey(LocalHubCity, on_delete=models.CASCADE, related_name='sea_terminals')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Морской терминал прибытия'
        verbose_name_plural = 'Морские терминалы прибытия'


class SeaLine(models.Model):
    name = models.CharField('Морская линия', max_length=32, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Морская линия'
        verbose_name_plural = 'Морские линии'


class SeaETD(models.Model):
    etd = models.DateField('Дата выхода судна')

    def __str__(self):
        return str(self.etd)

    class Meta:
        ordering = ['etd']
        verbose_name = 'Дата выхода судна'
        verbose_name_plural = 'Даты выхода судов'


class ForeignAgent(models.Model):
    title = models.CharField('Агент', max_length=64)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'Агент'
        verbose_name_plural = 'Агенты'

class SeaRate(models.Model):
    sea_line = models.ForeignKey(SeaLine, on_delete=models.CASCADE, related_name='sea_rates')
    sea_start_terminal = models.ForeignKey(SeaStartTerminal, on_delete=models.CASCADE, related_name='sea_rates')
    sea_end_terminal = models.ForeignKey(SeaEndTerminal, on_delete=models.CASCADE, related_name='sea_rates')
    etd = models.ManyToManyField(SeaETD, related_name='sea_rates', blank=True)
    validity = models.DateField('Валидность до')
    container = models.CharField('Тип КТК', max_length=16, choices=constants.CONTAINER_OPTIONS)
    rate_20 = models.DecimalField('Стоимость за 20ft, $', max_digits=9, decimal_places=2, null=True, blank=True)
    rate_40 = models.DecimalField('Стоимость за 40ft, $', max_digits=9, decimal_places=2, null=True, blank=True)
    intermediate = models.ForeignKey(SeaStartTerminal, on_delete=models.CASCADE, null=True, blank=True, related_name='start_point_rates')
    agent = models.ForeignKey(ForeignAgent, verbose_name='Агент', on_delete=models.CASCADE, null=True, blank=True, related_name='agents')
    conversion = models.FloatField(verbose_name='Конвертация, %')
    drop_off = models.ManyToManyField(LocalHubCity, verbose_name='Дроп офф', related_name='sea_rate_drop')
    

    class Meta:
        verbose_name = 'Морская ставка'
        verbose_name_plural = 'Морские ставки'

    def __str__(self):
        representation = f'{self.sea_start_terminal} - {self.sea_end_terminal}'
        return representation
    
    def get_etds(self):
        return ', '.join([etd.__str__() for etd in self.etd.all()])
    