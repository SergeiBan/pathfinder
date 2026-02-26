from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'paths'

urlpatterns = [
    path('', views.index, name='index'),
    path('sea_calculation/', views.sea_calculation, name='sea_calculation'),
    path('rr_calculation/', views.rr_calculation, name='rr_calculation'),
    path('sea_rr_calculation/', views.sea_rr_calculation, name='sea_rr_calculation'),
    path('upload/', views.file_upload, name='upload')
]
