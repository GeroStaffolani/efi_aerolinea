from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Vuelo, Reserva

def airline_context(request):
    return {
    'airline_name': _('GroPottFly'),
        'airline_slogan': _('Volamos hacia el futuro'),
        'total_vuelos_hoy': Vuelo.objects.filter(
            fecha_salida__date=timezone.now().date(),
            estado='programado'
        ).count() if 'timezone' in globals() else 0,
        'idiomas_disponibles': [
            {'code': 'es', 'name': 'Español'},
            {'code': 'en', 'name': 'English'},
        ]
    }
