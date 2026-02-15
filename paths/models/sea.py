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


class StartPortCity(models.Model):
    name = models.CharField('Город отправки судна', max_length=32, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Город отправки судна'
        verbose_name_plural = 'Города отправки судна'


class StartPort(models.Model):
    name = models.CharField('Порт отправки', choices=FOREIGN_PORTS, max_length=32, unique=True)
    city = models.ForeignKey(StartPortCity, on_delete=models.CASCADE, related_name='ports')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Порт отправки'
        verbose_name_plural = 'Порты отправки'


class LocalHubCity(models.Model):
    name = models.CharField('Портовый город прибытия', max_length=32, unique=True)

    def __str__(self):
            return self.name
    
    class Meta:
        verbose_name = 'Портовый город прибытия'
        verbose_name_plural = 'Портовые города прибытия'


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


class SeaRate(models.Model):
    sea_line = models.ForeignKey(SeaLine, on_delete=models.CASCADE, related_name='sea_rates')
    start_port = models.ForeignKey(StartPort, on_delete=models.CASCADE, related_name='sea_rates')
    sea_end_terminal = models.ForeignKey(SeaEndTerminal, on_delete=models.CASCADE, related_name='sea_rates')
    etd = models.ManyToManyField(SeaETD, related_name='sea_rates')
    validity = models.DateField('Валидность до')
    container = models.CharField('Тип КТК', max_length=16, choices=constants.CONTAINER_OPTIONS)
    rate = models.DecimalField('Стоимость', max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.rate)
    
    class Meta:
        verbose_name = 'Морская ставка'
        verbose_name_plural = 'Морские ставки'