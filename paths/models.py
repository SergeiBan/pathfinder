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


class ForeignPort(models.Model):
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



class EndCity(models.Model):
    name = models.CharField('Российский порт', max_length=32, unique=True)

    def __str__(self):
        return self.name


CITY_STATUS_OPTIONS = (
    ('Порт', 'is a port'),
    ('Автодоставка из порта', 'truck after port'),
    ('ЖД доставка из порта', 'RW after port')
)

class EndCity(models.Model):
    name = models.CharField('Город доставки', max_length=32, unique=True)
    rr_hub = models.ForeignKey(RRHub, on_delete=models.CASCADE, related_name='end_cities')
    logistic_status = models.CharField('Логистический статус', max_length=32, choices=CITY_STATUS_OPTIONS)

    def __str__(self):
        return self.name

class SeaLine(models.Model):
    name = models.CharField('Морская линия', max_length=32, unique=True)
    end_cities = models.ManyToManyField(EndCity, related_name='sea_lines')
    foreign_ports = models.ManyToManyField(ForeignPort, related_name='sea_lines')

    def __str__(self):
        return self.name


class SeaRate(models.Model):
    sea_line = models.ForeignKey(SeaLine, on_delete=models.CASCADE, related_name='sea_rates')
    foreign_port = models.ForeignKey(ForeignPort, on_delete=models.CASCADE, related_name='sea_rates')
    russian_port = models.ForeignKey(EndCity, on_delete=models.CASCADE, related_name='sea_rates')
    rate = models.DecimalField('Стоимость', max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.rate)

class Calculation(models.Model):
    foreign_port = models.ForeignKey(ForeignPort, on_delete=models.CASCADE, related_name='calculations')
    end_city = models.ForeignKey(EndCity, on_delete=models.CASCADE, related_name='calculations')
    cheapest = models.DecimalField('Самый дешевый', max_digits=9, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.end_city.logistic_status == 'Порт':
            self.cheapest = 0
            applicable_rates = SeaRate.objects.filter(foreign_port=self.foreign_port, russian_port=self.end_city)
            if applicable_rates:
                self.cheapest = applicable_rates.aggregate(min_cost=Min('rate'))['min_cost']
            
            print(self.cheapest)


        super().save(*args, **kwargs)
    