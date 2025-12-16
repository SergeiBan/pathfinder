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


class StartPort(models.Model):
    name = models.CharField('Порт отправки', choices=FOREIGN_PORTS, max_length=32, unique=True)

    def __str__(self):
        return self.name


class SeaEndTerminal(models.Model):
    name = models.CharField('Морской терминал прибытия', max_length=32, unique=True)

    def __str__(self):
        return self.name


class SeaLine(models.Model):
    name = models.CharField('Морская линия', max_length=32, unique=True)

    def __str__(self):
        return self.name

class SeaETD(models.Model):
    etd = models.DateField('Дата выхода судна')

    class Meta:
        ordering = ['etd']

    def __str__(self):
        return str(self.etd)


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