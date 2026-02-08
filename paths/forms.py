from django import forms
from .models import SeaCalculation, RRCalculation, SeaRRCalculation, RREndCity, RREndTerminal


class SeaCalculationForm(forms.ModelForm):
    
    class Meta:
        model = SeaCalculation
        fields = ('start_port', 'sea_end_terminal', 'etd_from', 'etd_to', 'container')

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

    rr_end_city = forms.ModelChoiceField(
        queryset=RREndCity.objects.all(),
        label='Если считаем ЖД до города',
        required=False
    )
    rr_end_terminal = forms.ModelChoiceField(
        queryset=RREndTerminal.objects.all(),
        label='Если считаем ЖД до терминала',
        required=False
    )
    
    class Meta:
        model = SeaRRCalculation
        fields = ('start_port', 'sea_end_terminal', 'etd_from', 'etd_to', 'truck_end_city', 'container', 'gross', 'is_VTT')

        widgets = {
            'etd_from': forms.DateInput(attrs={'type': 'date'}),
            'etd_to': forms.DateInput(attrs={'type': 'date'}),
        }