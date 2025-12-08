from django.forms import ModelForm
from .models import StartCity


class StartCityForm(ModelForm):
    
    class Meta:
        model = StartCity
        fields = ("name",)
