from django.db import models
from django.db.models import Avg, Min


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



class RRHub(models.Model):
    name = models.CharField('ЖД хаб', max_length=32, unique=True)

    def __str__(self):
        return self.name


class RRStation(models.Model):
    name = models.CharField('ЖД станция', max_length=32, unique=True)
    price = models.DecimalField('Цена', max_digits=9, decimal_places=2)
    rr_hub = models.ForeignKey(RRHub, on_delete=models.CASCADE, related_name='rr_stations')

    def __str__(self):
        return self.name



class EndPort(models.Model):
    name = models.CharField('Порт', max_length=32, unique=True)

    def __str__(self):
        return self.name


class EndPortSatellite(models.Model):
    name = models.CharField('Сателлит порта', max_length=32, unique=True)
    end_port = models.ForeignKey(EndPort, on_delete=models.CASCADE, related_name='satellites')

    def __str__(self):
        return self.name


class InlandEndCity(models.Model):
    name = models.CharField('Город удаленный от порта', max_length=32, unique=True)
    rr_hub = models.ForeignKey(RRHub, on_delete=models.CASCADE, related_name='inland_cities')

    def __str__(self):
        return self.name


class SeaLine(models.Model):
    name = models.CharField('Морская линия', max_length=32, unique=True)
    start_ports = models.ManyToManyField(StartPort, related_name='sea_lines')
    end_ports = models.ManyToManyField(EndPort, related_name='sea_lines')

    def __str__(self):
        return self.name


class SeaRate(models.Model):
    sea_line = models.ForeignKey(SeaLine, on_delete=models.CASCADE, related_name='sea_rates')
    start_port = models.ForeignKey(StartPort, on_delete=models.CASCADE, related_name='sea_rates')
    end_port = models.ForeignKey(EndPort, on_delete=models.CASCADE, related_name='sea_rates')
    rate = models.DecimalField('Стоимость', max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.rate)


class Calculation(models.Model):
    start_port = models.ForeignKey(StartPort, on_delete=models.CASCADE, related_name='calculations')
    endpoint_name = models.CharField('Город доставки', max_length=32)
    cheapest = models.DecimalField('Самый дешевый', max_digits=9, decimal_places=2)

    def save(self, *args, **kwargs):
        self.cheapest = 0
        end_port = EndPort.objects.filter(name=self.endpoint_name)
        if end_port:
            end_port = end_port.first()
        
            applicable_rates = SeaRate.objects.filter(start_port=self.start_port, end_port__name=self.endpoint_name)
            if applicable_rates:
                self.cheapest = applicable_rates.aggregate(min_cost=Min('rate'))['min_cost']
            
            print(self.cheapest)


        super().save(*args, **kwargs)
    