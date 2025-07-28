from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Pasajero, Reserva, Vuelo
from datetime import date

class PasajeroForm(forms.ModelForm):
    class Meta:
        model = Pasajero
        fields = ['nombre', 'documento', 'tipo_documento', 'email', 'telefono', 'fecha_nacimiento']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Nombre completo')}),
            'documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Número de documento')}),
            'tipo_documento': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email')}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Teléfono')}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_fecha_nacimiento(self):
        fecha = self.cleaned_data['fecha_nacimiento']
        if fecha > date.today():
            raise forms.ValidationError(_('La fecha de nacimiento no puede ser futura'))
        return fecha

class BuscarVuelosForm(forms.Form):
    origen = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ciudad de origen')})
    )
    destino = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Ciudad de destino')})
    )
    fecha_salida = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    pasajeros = forms.IntegerField(
        min_value=1,
        max_value=10,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['asiento']
        widgets = {
            'asiento': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        vuelo = kwargs.pop('vuelo', None)
        super().__init__(*args, **kwargs)
        if vuelo:
            # Solo mostrar asientos disponibles para este vuelo
            asientos_ocupados = Reserva.objects.filter(
                vuelo=vuelo, 
                estado__in=['confirmada', 'pendiente']
            ).values_list('asiento_id', flat=True)
            
            self.fields['asiento'].queryset = vuelo.avion.asientos.exclude(
                id__in=asientos_ocupados
            ).filter(estado='disponible')
