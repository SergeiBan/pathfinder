from django.db import models
from django.db.models import Avg


START_CITIES = (
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


class StartCity(models.Model):
    name = models.CharField('Город отправки', choices=START_CITIES, max_length=32, unique=True)

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
    name = models.CharField('Город доставки', max_length=32, unique=True)
    rr_hub = models.ForeignKey(RRHub, on_delete=models.CASCADE, related_name='end_cities')

    def __str__(self):
        return self.name


class Calculation(models.Model):
    start_city = models.ForeignKey(StartCity, on_delete=models.CASCADE, related_name='calculations')
    end_city = models.ForeignKey(EndCity, on_delete=models.CASCADE, related_name='calculations')
    rr_cost = models.DecimalField('Средняя стоимость ЖД', max_digits=9, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.rr_cost = self.end_city.rr_hub.rr_stations.aggregate(Avg('price'))['price__avg']
        super().save(*args, **kwargs)
    