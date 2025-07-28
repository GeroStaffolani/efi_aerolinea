#!/usr/bin/env python
"""
Script para crear datos de ejemplo en el sistema de aerolínea
"""
import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'airline_system.settings')
django.setup()

from flights.models import Avion, Vuelo, Pasajero, Asiento, Reserva, Boleto
from django.contrib.auth.models import User

def crear_datos_ejemplo():
    """Crear datos de ejemplo para el sistema"""
    
    print("Creando datos de ejemplo...")
    
    # Crear superusuario si no existe
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✓ Superusuario creado: admin/admin123")
    
    # Crear aviones
    aviones_data = [
        {'modelo': 'Boeing 737-800', 'filas': 32, 'columnas': 6},
        {'modelo': 'Airbus A320', 'filas': 28, 'columnas': 6},
        {'modelo': 'Boeing 777-300', 'filas': 42, 'columnas': 9},
        {'modelo': 'Embraer E190', 'filas': 19, 'columnas': 4},
    ]
    
    aviones = []
    for data in aviones_data:
        avion, created = Avion.objects.get_or_create(
            modelo=data['modelo'],
            defaults={
                'filas': data['filas'],
                'columnas': data['columnas'],
                'capacidad': data['filas'] * data['columnas']
            }
        )
        aviones.append(avion)
        if created:
            print(f"✓ Avión creado: {avion.modelo}")
    
    # Crear vuelos
    ciudades = [
        'Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao',
        'París', 'Londres', 'Roma', 'Berlín', 'Amsterdam'
    ]
    
    vuelos_creados = 0
    for i in range(20):
        origen = ciudades[i % len(ciudades)]
        destino = ciudades[(i + 1) % len(ciudades)]
        
        if origen != destino:
            fecha_salida = datetime.now() + timedelta(days=i % 30 + 1, hours=i % 12 + 6)
            fecha_llegada = fecha_salida + timedelta(hours=2 + i % 4)
            
            vuelo, created = Vuelo.objects.get_or_create(
                codigo_vuelo=f'AE{1000 + i}',
                defaults={
                    'avion': aviones[i % len(aviones)],
                    'origen': origen,
                    'destino': destino,
                    'fecha_salida': fecha_salida,
                    'fecha_llegada': fecha_llegada,
                    'duracion': fecha_llegada - fecha_salida,
                    'precio_base': Decimal(str(100 + i * 10)),
                    'estado': 'programado'
                }
            )
            if created:
                vuelos_creados += 1
    
    print(f"✓ {vuelos_creados} vuelos creados")
    
    # Crear pasajeros de ejemplo
    pasajeros_data = [
        {
            'nombre': 'Juan Pérez García',
            'documento': '12345678A',
            'tipo_documento': 'dni',
            'email': 'juan.perez@email.com',
            'telefono': '+34 600 123 456',
            'fecha_nacimiento': datetime(1985, 5, 15).date()
        },
        {
            'nombre': 'María González López',
            'documento': '87654321B',
            'tipo_documento': 'dni',
            'email': 'maria.gonzalez@email.com',
            'telefono': '+34 600 654 321',
            'fecha_nacimiento': datetime(1990, 8, 22).date()
        },
        {
            'nombre': 'Carlos Rodríguez Martín',
            'documento': 'P123456789',
            'tipo_documento': 'pasaporte',
            'email': 'carlos.rodriguez@email.com',
            'telefono': '+34 600 789 123',
            'fecha_nacimiento': datetime(1978, 12, 3).date()
        }
    ]
    
    pasajeros_creados = 0
    for data in pasajeros_data:
        pasajero, created = Pasajero.objects.get_or_create(
            documento=data['documento'],
            defaults=data
        )
        if created:
            pasajeros_creados += 1
    
    print(f"✓ {pasajeros_creados} pasajeros creados")
    
    # Crear algunas reservas de ejemplo
    vuelos = Vuelo.objects.filter(estado='programado')[:5]
    pasajeros = Pasajero.objects.all()
    
    reservas_creadas = 0
    for i, vuelo in enumerate(vuelos):
        if i < len(pasajeros):
            pasajero = pasajeros[i]
            asientos_disponibles = vuelo.avion.asientos.filter(estado='disponible')
            
            if asientos_disponibles.exists():
                asiento = asientos_disponibles.first()
                
                reserva, created = Reserva.objects.get_or_create(
                    vuelo=vuelo,
                    pasajero=pasajero,
                    defaults={
                        'asiento': asiento,
                        'estado': 'confirmada'
                    }
                )
                
                if created:
                    # Crear boleto automáticamente
                    Boleto.objects.get_or_create(reserva=reserva)
                    
                    # Actualizar estado del asiento
                    asiento.estado = 'ocupado'
                    asiento.save()
                    
                    reservas_creadas += 1
    
    print(f"✓ {reservas_creadas} reservas creadas")
    print("\n¡Datos de ejemplo creados exitosamente!")
    print("\nCredenciales de administrador:")
    print("Usuario: admin")
    print("Contraseña: admin123")
    print("\nPuedes acceder al panel de administración en: /admin/")

if __name__ == '__main__':
    crear_datos_ejemplo()
