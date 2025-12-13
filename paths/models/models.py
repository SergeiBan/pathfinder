



# class StartRRHub(models.Model):
#     name = models.CharField('ЖД хаб отправки', choices=FOREIGN_PORTS, max_length=32, unique=True)

#     def __str__(self):
#         return self.name

# class RRHub(models.Model):
#     name = models.CharField('ЖД хаб', max_length=32, unique=True)

#     def __str__(self):
#         return self.name


# class RRStation(models.Model):
#     name = models.CharField('ЖД станция', max_length=32, unique=True)
#     price = models.DecimalField('Цена', max_digits=9, decimal_places=2)
#     rr_hub = models.ForeignKey(RRHub, on_delete=models.CASCADE, related_name='rr_stations')

#     def __str__(self):
#         return self.name






# class RREndRate(models.Model):
#     end_port = models.ForeignKey(EndPort, on_delete=models.CASCADE, related_name='rr_end_rates')
#     rr_hub = models.ForeignKey(RRHub, on_delete=models.CASCADE, related_name='rr_end_rates')
#     rate = models.DecimalField('Стоимость', max_digits=9, decimal_places=2)


# class RRDirectRate(models.Model):
#     start_rr_hub = models.ForeignKey(StartRRHub, on_delete=models.CASCADE, related_name='rr_direct_rates')
#     rr_end_hub = models.ForeignKey(RRHub, on_delete=models.CASCADE, related_name='rr_end_rates')


# class EndPortSatellite(models.Model):
#     name = models.CharField('Сателлит порта', max_length=32, unique=True)
#     end_port = models.ForeignKey(EndPort, on_delete=models.CASCADE, related_name='satellites')

#     def __str__(self):
#         return self.name


# class InlandEndCity(models.Model):
#     name = models.CharField('Город удаленный от порта', max_length=32, unique=True)
#     rr_hub = models.ForeignKey(RRHub, on_delete=models.CASCADE, related_name='inland_cities')

#     def __str__(self):
#         return self.name







