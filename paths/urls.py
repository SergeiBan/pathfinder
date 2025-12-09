from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'paths'

urlpatterns = [
    path('', views.index, name='index'),
]
