from django import forms
from .models import SeaCalculation, RRCalculation, SeaRRCalculation, RREndTerminal


class SeaCalculationForm(forms.ModelForm):
    
    class Meta:
        model = SeaCalculation
        fields = ('sea_start_terminal', 'sea_end_terminal', 'etd_from', 'etd_to', 'container')

        widgets = {
            'etd_from': forms.DateInput(attrs={'type': 'date'}),
            'etd_to': forms.DateInput(attrs={'type': 'date'}),
        }


class RRCalculationForm(forms.ModelForm):
    
    class Meta:
        model = RRCalculation
        fields = ('start_city', 'end_city', 'etd_from', 'etd_to', 'container')

        widgets = {
            'etd_from': forms.DateInput(attrs={'type': 'date'}),
            'etd_to': forms.DateInput(attrs={'type': 'date'}),
        }


MODALITY_CHOICES = (
    ('all', 'Все'),
    ('sea_rr', 'Море + ЖД'),
    ('sea', 'Море'),
    ('rr', 'ЖД')
)
class ModalityForm(forms.Form):
    modality = forms.ChoiceField(
        label='Транспорт',
        choices=MODALITY_CHOICES,
    )


class SeaRRCalculationForm(forms.ModelForm):

    rr_end_terminal = forms.ModelChoiceField(
        queryset=RREndTerminal.objects.all(),
        label='Если нужен конкретный ЖД терминал',
        required=False
    )
    
    class Meta:
        model = SeaRRCalculation
        fields = ('sea_start_terminal', 'etd_from', 'etd_to', 'end_city', 'container', 'gross', 'is_VTT')

        widgets = {
            'etd_from': forms.DateInput(attrs={'type': 'date'}),
            'etd_to': forms.DateInput(attrs={'type': 'date'}),
        }