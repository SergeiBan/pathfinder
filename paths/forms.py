from django import forms
from .models import SeaCalculation, RRCalculation, SeaRRCalculation, InnerRRTerminal


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
        queryset=InnerRRTerminal.objects.all(),
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

    def clean(self):
        cleaned_data = super().clean()
        rr_end_terminal = cleaned_data.get("rr_end_terminal")
        end_city = cleaned_data.get("end_city")

        if rr_end_terminal and rr_end_terminal not in end_city.rr_terminals.all():
            raise forms.ValidationError("Выбранный ЖД терминал не относится к выбранному городу")
        return cleaned_data