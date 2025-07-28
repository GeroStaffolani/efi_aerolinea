from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.utils.translation import gettext as _
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Vuelo, Pasajero, Reserva, Asiento, Boleto
from .forms import PasajeroForm, BuscarVuelosForm, ReservaForm
from .services import ReservaService, VueloService, ReporteService
import json
from datetime import datetime, date

def home(request):
    """Vista principal del sistema"""
    vuelos_destacados = Vuelo.objects.filter(
        estado='programado',
        fecha_salida__gte=datetime.now()
    ).order_by('fecha_salida')[:6]
    
    context = {
        'vuelos_destacados': vuelos_destacados,
        'total_vuelos': Vuelo.objects.count(),
        'total_pasajeros': Pasajero.objects.count(),
        'total_reservas': Reserva.objects.count(),
    }
    return render(request, 'flights/home.html', context)

def buscar_vuelos(request):
    """Vista para buscar vuelos disponibles"""
    form = BuscarVuelosForm()
    vuelos = []
    
    if request.method == 'POST':
        form = BuscarVuelosForm(request.POST)
        if form.is_valid():
            origen = form.cleaned_data['origen']
            destino = form.cleaned_data['destino']
            fecha_salida = form.cleaned_data['fecha_salida']
            pasajeros = form.cleaned_data['pasajeros']
            
            vuelos = VueloService.buscar_vuelos_disponibles(
                origen, destino, fecha_salida, pasajeros
            )
    
    context = {
        'form': form,
        'vuelos': vuelos,
    }
    return render(request, 'flights/buscar_vuelos.html', context)

def detalle_vuelo(request, vuelo_id):
    """Vista detallada de un vuelo específico"""
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    asientos_disponibles = vuelo.asientos_disponibles()
    
    # Obtener layout de asientos
    asientos = vuelo.avion.asientos.all().order_by('fila', 'columna')
    asientos_ocupados = Reserva.objects.filter(
        vuelo=vuelo,
        estado__in=['confirmada', 'pendiente']
    ).values_list('asiento_id', flat=True)
    
    context = {
        'vuelo': vuelo,
        'asientos_disponibles': asientos_disponibles,
        'asientos': asientos,
        'asientos_ocupados': list(asientos_ocupados),
    }
    return render(request, 'flights/detalle_vuelo.html', context)

@login_required
def crear_reserva(request, vuelo_id):
    """Vista para crear una nueva reserva"""
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    
    if request.method == 'POST':
        pasajero_form = PasajeroForm(request.POST)
        reserva_form = ReservaForm(request.POST, vuelo=vuelo)
        
        if pasajero_form.is_valid() and reserva_form.is_valid():
            try:
                # Buscar o crear pasajero
                pasajero, created = Pasajero.objects.get_or_create(
                    documento=pasajero_form.cleaned_data['documento'],
                    defaults=pasajero_form.cleaned_data
                )
                
                # Crear reserva usando el servicio
                reserva = ReservaService.crear_reserva(
                    vuelo=vuelo,
                    pasajero=pasajero,
                    asiento=reserva_form.cleaned_data['asiento']
                )
                
                messages.success(request, _('Reserva creada exitosamente'))
                return redirect('detalle_reserva', reserva_id=reserva.id)
                
            except Exception as e:
                messages.error(request, str(e))
    else:
        pasajero_form = PasajeroForm()
        reserva_form = ReservaForm(vuelo=vuelo)
    
    context = {
        'vuelo': vuelo,
        'pasajero_form': pasajero_form,
        'reserva_form': reserva_form,
    }
    return render(request, 'flights/crear_reserva.html', context)

@login_required
def detalle_reserva(request, reserva_id):
    """Vista detallada de una reserva"""
    reserva = get_object_or_404(Reserva, id=reserva_id)
    
    context = {
        'reserva': reserva,
    }
    return render(request, 'flights/detalle_reserva.html', context)

@login_required
def mis_reservas(request):
    """Vista para mostrar las reservas del usuario"""
    # En un sistema real, filtrarías por usuario
    reservas = Reserva.objects.all().order_by('-fecha_reserva')
    
    paginator = Paginator(reservas, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'flights/mis_reservas.html', context)

@login_required
def cancelar_reserva(request, reserva_id):
    """Vista para cancelar una reserva"""
    reserva = get_object_or_404(Reserva, id=reserva_id)
    
    if request.method == 'POST':
        try:
            ReservaService.cancelar_reserva(reserva)
            messages.success(request, _('Reserva cancelada exitosamente'))
        except Exception as e:
            messages.error(request, str(e))
        
        return redirect('mis_reservas')
    
    context = {
        'reserva': reserva,
    }
    return render(request, 'flights/cancelar_reserva.html', context)

@login_required
def reportes(request):
    """Vista para mostrar reportes del sistema"""
    if not request.user.is_staff:
        messages.error(request, _('No tienes permisos para acceder a esta sección'))
        return redirect('home')
    
    # Estadísticas generales
    stats = ReporteService.obtener_estadisticas_generales()
    
    # Vuelos más populares
    vuelos_populares = ReporteService.obtener_vuelos_populares()
    
    context = {
        'stats': stats,
        'vuelos_populares': vuelos_populares,
    }
    return render(request, 'flights/reportes.html', context)

@login_required
def reporte_pasajeros_vuelo(request, vuelo_id):
    """Vista para mostrar el reporte de pasajeros por vuelo"""
    if not request.user.is_staff:
        messages.error(request, _('No tienes permisos para acceder a esta sección'))
        return redirect('home')
    
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    pasajeros = ReporteService.obtener_pasajeros_por_vuelo(vuelo)
    
    context = {
        'vuelo': vuelo,
        'pasajeros': pasajeros,
    }
    return render(request, 'flights/reporte_pasajeros_vuelo.html', context)

def registro(request):
    """Vista para registro de usuarios"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada para {username}')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'registration/registro.html', context)

def obtener_asientos_ajax(request, vuelo_id):
    """Vista AJAX para obtener asientos disponibles"""
    vuelo = get_object_or_404(Vuelo, id=vuelo_id)
    
    asientos = []
    asientos_ocupados = Reserva.objects.filter(
        vuelo=vuelo,
        estado__in=['confirmada', 'pendiente']
    ).values_list('asiento_id', flat=True)
    
    for asiento in vuelo.avion.asientos.all():
        asientos.append({
            'id': asiento.id,
            'numero': asiento.numero,
            'fila': asiento.fila,
            'columna': asiento.columna,
            'tipo': asiento.tipo,
            'disponible': asiento.id not in asientos_ocupados
        })
    
    return JsonResponse({'asientos': asientos})
