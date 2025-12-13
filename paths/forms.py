from django import forms
from .models import SeaCalculation


class SeaCalculationForm(forms.ModelForm):
    
    class Meta:
        model = SeaCalculation
        fields = ('start_port', 'sea_end_terminal', 'etd', 'container')

        widgets = {
            'etd': forms.DateInput(attrs={'type': 'date'}),
        }

