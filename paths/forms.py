from django import forms
from .models import Calculation


class CalculationForm(forms.ModelForm):
    
    class Meta:
        model = Calculation
        fields = ('foreign_port', 'end_city')

