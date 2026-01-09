from django import forms
from .models import SeaCalculation


class SeaCalculationForm(forms.ModelForm):
    
    class Meta:
        model = SeaCalculation
        fields = ('start_port', 'sea_end_terminal', 'etd_from', 'etd_to', 'container')

        widgets = {
            'etd_from': forms.DateInput(attrs={'type': 'date'}),
            'etd_to': forms.DateInput(attrs={'type': 'date'}),
        }


MODALITY_CHOICES = (
    ('all', 'Все'),
    ('sea', 'Море'),
    ('rr', 'ЖД')
)
class ModalityForm(forms.Form):
    modality = forms.ChoiceField(
        label='Транспорт',
        choices=MODALITY_CHOICES,
    )