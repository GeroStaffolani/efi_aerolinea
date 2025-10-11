from django.db import transaction
from django.utils.translation import gettext as _
from django.db.models import Count, Q, F
from .models import Vuelo, Reserva, Pasajero, Boleto, Asiento
from datetime import datetime, date

class VueloService:
    """Servicio para manejar la lógica de negocio de vuelos"""
    
    @staticmethod
    def buscar_vuelos_disponibles(origen, destino, fecha_salida, num_pasajeros):
        """Busca vuelos disponibles según los criterios especificados"""
        vuelos = Vuelo.objects.filter(
            origen__icontains=origen,
            destino__icontains=destino,
            fecha_salida__date=fecha_salida,
            estado='programado'
        ).annotate(
            asientos_ocupados=Count('reservas', filter=Q(reservas__estado='confirmada'))
        ).filter(
            asientos_ocupados__lt=F('avion__capacidad') - num_pasajeros + 1
        )
        
        return vuelos

    @staticmethod
    def obtener_asientos_disponibles(vuelo):
        """Obtiene los asientos disponibles para un vuelo"""
        asientos_ocupados = Reserva.objects.filter(
            vuelo=vuelo,
            estado__in=['confirmada', 'pendiente']
        ).values_list('asiento_id', flat=True)
        
        return vuelo.avion.asientos.exclude(id__in=asientos_ocupados)

class ReservaService:
    """Servicio para manejar la lógica de negocio de reservas"""
    
    @staticmethod
    @transaction.atomic
    def crear_reserva(vuelo, pasajero, asiento):
        """Crea una nueva reserva de forma transaccional"""
        from rest_framework.exceptions import ValidationError
        # Verificar que el asiento esté disponible
        if Reserva.objects.filter(
            vuelo=vuelo,
            asiento=asiento,
            estado__in=['confirmada', 'pendiente']
        ).exists():
            raise ValidationError(_('El asiento seleccionado ya no está disponible'))
        # Verificar que el pasajero no tenga ya una reserva para este vuelo
        if Reserva.objects.filter(
            vuelo=vuelo,
            pasajero=pasajero,
            estado__in=['confirmada', 'pendiente']
        ).exists():
            raise ValidationError(_('El pasajero ya tiene una reserva para este vuelo'))
        # Crear la reserva
        reserva = Reserva.objects.create(
            vuelo=vuelo,
            pasajero=pasajero,
            asiento=asiento,
            estado='confirmada'
        )
        # Crear el boleto automáticamente
        Boleto.objects.create(reserva=reserva)
        # Actualizar estado del asiento
        asiento.estado = 'ocupado'
        asiento.save()
        return reserva
    
    @staticmethod
    @transaction.atomic
    def cancelar_reserva(reserva):
        """Cancela una reserva existente"""
        from rest_framework.exceptions import ValidationError
        if reserva.estado == 'cancelada':
            raise ValidationError(_('La reserva ya está cancelada'))
        # Actualizar estado de la reserva
        reserva.estado = 'cancelada'
        reserva.save()
        # Liberar el asiento
        reserva.asiento.estado = 'disponible'
        reserva.asiento.save()
        # Cancelar el boleto si existe
        if hasattr(reserva, 'boleto'):
            reserva.boleto.estado = 'cancelado'
            reserva.boleto.save()
        return reserva
    
    @staticmethod
    def confirmar_reserva(reserva):
        """Confirma una reserva pendiente"""
        if reserva.estado != 'pendiente':
            raise ValueError(_('Solo se pueden confirmar reservas pendientes'))
        
        reserva.estado = 'confirmada'
        reserva.save()
        
        return reserva

class ReporteService:
    """Servicio para generar reportes del sistema"""
    
    @staticmethod
    def obtener_estadisticas_generales():
        """Obtiene estadísticas generales del sistema"""
        return {
            'total_vuelos': Vuelo.objects.count(),
            'vuelos_activos': Vuelo.objects.filter(estado='programado').count(),
            'total_pasajeros': Pasajero.objects.count(),
            'total_reservas': Reserva.objects.count(),
            'reservas_confirmadas': Reserva.objects.filter(estado='confirmada').count(),
            'reservas_canceladas': Reserva.objects.filter(estado='cancelada').count(),
        }
    
    @staticmethod
    def obtener_vuelos_populares(limite=10):
        """Obtiene los vuelos más populares por número de reservas"""
        return Vuelo.objects.annotate(
            num_reservas=Count('reservas', filter=Q(reservas__estado='confirmada'))
        ).order_by('-num_reservas')[:limite]
    
    @staticmethod
    def obtener_pasajeros_por_vuelo(vuelo):
        """Obtiene la lista de pasajeros para un vuelo específico"""
        return Reserva.objects.filter(
            vuelo=vuelo,
            estado='confirmada'
        ).select_related('pasajero', 'asiento').order_by('asiento__numero')
    
    @staticmethod
    def obtener_ocupacion_por_mes():
        """Obtiene estadísticas de ocupación por mes"""
        from django.db.models import Count
        from django.db.models.functions import TruncMonth
        
        return Reserva.objects.filter(
            estado='confirmada'
        ).annotate(
            mes=TruncMonth('fecha_reserva')
        ).values('mes').annotate(
            total_reservas=Count('id')
        ).order_by('mes')
