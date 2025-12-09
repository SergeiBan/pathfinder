from django import forms
from .models import Calculation


class CalculationForm(forms.ModelForm):
    
    class Meta:
        model = Calculation
        fields = ('start_port', 'endpoint_name')

