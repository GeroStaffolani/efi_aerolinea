from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Avion, Vuelo, Pasajero, Asiento, Reserva, Boleto

@admin.register(Avion)
class AvionAdmin(admin.ModelAdmin):
    list_display = ['modelo', 'capacidad', 'filas', 'columnas', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['modelo']
    readonly_fields = ['capacidad', 'fecha_creacion']

@admin.register(Vuelo)
class VueloAdmin(admin.ModelAdmin):
    list_display = ['codigo_vuelo', 'origen', 'destino', 'fecha_salida', 'estado', 'precio_base']
    list_filter = ['estado', 'origen', 'destino', 'fecha_salida']
    search_fields = ['codigo_vuelo', 'origen', 'destino']
    date_hierarchy = 'fecha_salida'
    readonly_fields = ['fecha_creacion']

@admin.register(Pasajero)
class PasajeroAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'documento', 'tipo_documento', 'email', 'telefono']
    list_filter = ['tipo_documento', 'fecha_registro']
    search_fields = ['nombre', 'documento', 'email']
    readonly_fields = ['fecha_registro']

@admin.register(Asiento)
class AsientoAdmin(admin.ModelAdmin):
    list_display = ['avion', 'numero', 'fila', 'columna', 'tipo', 'estado']
    list_filter = ['tipo', 'estado', 'avion']
    search_fields = ['numero', 'avion__modelo']

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['codigo_reserva', 'vuelo', 'pasajero', 'asiento', 'estado', 'precio']
    list_filter = ['estado', 'fecha_reserva', 'vuelo__origen', 'vuelo__destino']
    search_fields = ['codigo_reserva', 'pasajero__nombre', 'vuelo__codigo_vuelo']
    readonly_fields = ['codigo_reserva', 'fecha_reserva']

@admin.register(Boleto)
class BoletoAdmin(admin.ModelAdmin):
    list_display = ['codigo_barra', 'reserva', 'estado', 'fecha_emision']
    list_filter = ['estado', 'fecha_emision']
    search_fields = ['codigo_barra', 'reserva__codigo_reserva']
    readonly_fields = ['codigo_barra', 'fecha_emision']
