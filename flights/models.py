from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
import uuid
from datetime import datetime

class Avion(models.Model):
    modelo = models.CharField(_('Modelo'), max_length=100)
    capacidad = models.PositiveIntegerField(_('Capacidad'))
    filas = models.PositiveIntegerField(_('Filas'), validators=[MinValueValidator(1), MaxValueValidator(50)])
    columnas = models.PositiveIntegerField(_('Columnas'), validators=[MinValueValidator(1), MaxValueValidator(10)])
    fecha_creacion = models.DateTimeField(_('Fecha de Creación'), auto_now_add=True)
    activo = models.BooleanField(_('Activo'), default=True)

    class Meta:
        verbose_name = _('Avión')
        verbose_name_plural = _('Aviones')

    def __str__(self):
        return f"{self.modelo} - {self.capacidad} asientos"

    def save(self, *args, **kwargs):
        if not self.capacidad:
            self.capacidad = self.filas * self.columnas
        super().save(*args, **kwargs)
        
        # Crear asientos automáticamente
        if not self.asientos.exists():
            self.crear_asientos()

    def crear_asientos(self):
        """Crear asientos automáticamente basado en filas y columnas"""
        letras = 'ABCDEFGHIJ'
        for fila in range(1, self.filas + 1):
            for col in range(self.columnas):
                numero = f"{fila}{letras[col]}"
                tipo = 'primera' if fila <= 3 else 'economica'
                Asiento.objects.create(
                    avion=self,
                    numero=numero,
                    fila=fila,
                    columna=letras[col],
                    tipo=tipo
                )

class Vuelo(models.Model):
    ESTADOS_VUELO = [
        ('programado', _('Programado')),
        ('abordando', _('Abordando')),
        ('en_vuelo', _('En Vuelo')),
        ('aterrizado', _('Aterrizado')),
        ('cancelado', _('Cancelado')),
        ('retrasado', _('Retrasado')),
    ]

    avion = models.ForeignKey(Avion, on_delete=models.CASCADE, related_name='vuelos', verbose_name=_('Avión'))
    codigo_vuelo = models.CharField(_('Código de Vuelo'), max_length=10, unique=True)
    origen = models.CharField(_('Origen'), max_length=100)
    destino = models.CharField(_('Destino'), max_length=100)
    fecha_salida = models.DateTimeField(_('Fecha de Salida'))
    fecha_llegada = models.DateTimeField(_('Fecha de Llegada'))
    duracion = models.DurationField(_('Duración'))
    estado = models.CharField(_('Estado'), max_length=20, choices=ESTADOS_VUELO, default='programado')
    precio_base = models.DecimalField(_('Precio Base'), max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(_('Fecha de Creación'), auto_now_add=True)

    class Meta:
        verbose_name = _('Vuelo')
        verbose_name_plural = _('Vuelos')
        ordering = ['fecha_salida']

    def __str__(self):
        return f"{self.codigo_vuelo} - {self.origen} → {self.destino}"

    def asientos_disponibles(self):
        """Retorna el número de asientos disponibles"""
        return self.avion.asientos.filter(
            reservas__isnull=True
        ).count()

    def asientos_ocupados(self):
        """Retorna el número de asientos ocupados"""
        return self.reservas.filter(estado='confirmada').count()

class Pasajero(models.Model):
    TIPOS_DOCUMENTO = [
        ('dni', _('DNI')),
        ('pasaporte', _('Pasaporte')),
        ('cedula', _('Cédula')),
    ]

    nombre = models.CharField(_('Nombre Completo'), max_length=200)
    documento = models.CharField(_('Documento'), max_length=20, unique=True)
    tipo_documento = models.CharField(_('Tipo de Documento'), max_length=20, choices=TIPOS_DOCUMENTO)
    email = models.EmailField(_('Email'))
    telefono = models.CharField(_('Teléfono'), max_length=20)
    fecha_nacimiento = models.DateField(_('Fecha de Nacimiento'))
    fecha_registro = models.DateTimeField(_('Fecha de Registro'), auto_now_add=True)

    class Meta:
        verbose_name = _('Pasajero')
        verbose_name_plural = _('Pasajeros')

    def __str__(self):
        return f"{self.nombre} - {self.documento}"

    def historial_vuelos(self):
        """Retorna el historial de vuelos del pasajero"""
        return self.reservas.filter(estado='confirmada').select_related('vuelo')

class Asiento(models.Model):
    TIPOS_ASIENTO = [
        ('primera', _('Primera Clase')),
        ('ejecutiva', _('Clase Ejecutiva')),
        ('economica', _('Clase Económica')),
    ]

    ESTADOS_ASIENTO = [
        ('disponible', _('Disponible')),
        ('reservado', _('Reservado')),
        ('ocupado', _('Ocupado')),
        ('mantenimiento', _('Mantenimiento')),
    ]

    avion = models.ForeignKey(Avion, on_delete=models.CASCADE, related_name='asientos', verbose_name=_('Avión'))
    numero = models.CharField(_('Número'), max_length=10)
    fila = models.PositiveIntegerField(_('Fila'))
    columna = models.CharField(_('Columna'), max_length=1)
    tipo = models.CharField(_('Tipo'), max_length=20, choices=TIPOS_ASIENTO, default='economica')
    estado = models.CharField(_('Estado'), max_length=20, choices=ESTADOS_ASIENTO, default='disponible')

    class Meta:
        verbose_name = _('Asiento')
        verbose_name_plural = _('Asientos')
        unique_together = ['avion', 'numero']

    def __str__(self):
        return f"{self.avion.modelo} - {self.numero}"

class Reserva(models.Model):
    ESTADOS_RESERVA = [
        ('pendiente', _('Pendiente')),
        ('confirmada', _('Confirmada')),
        ('cancelada', _('Cancelada')),
        ('completada', _('Completada')),
    ]

    vuelo = models.ForeignKey(Vuelo, on_delete=models.CASCADE, related_name='reservas', verbose_name=_('Vuelo'))
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE, related_name='reservas', verbose_name=_('Pasajero'))
    asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE, related_name='reservas', verbose_name=_('Asiento'))
    estado = models.CharField(_('Estado'), max_length=20, choices=ESTADOS_RESERVA, default='pendiente')
    fecha_reserva = models.DateTimeField(_('Fecha de Reserva'), auto_now_add=True)
    precio = models.DecimalField(_('Precio'), max_digits=10, decimal_places=2)
    codigo_reserva = models.CharField(_('Código de Reserva'), max_length=20, unique=True)

    class Meta:
        verbose_name = _('Reserva')
        verbose_name_plural = _('Reservas')
        unique_together = ['vuelo', 'pasajero']

    def __str__(self):
        return f"{self.codigo_reserva} - {self.pasajero.nombre}"

    def save(self, *args, **kwargs):
        if not self.codigo_reserva:
            self.codigo_reserva = str(uuid.uuid4())[:8].upper()
        if not self.precio:
            self.precio = self.calcular_precio()
        super().save(*args, **kwargs)

    def calcular_precio(self):
        """Calcula el precio basado en el tipo de asiento"""
        precio_base = self.vuelo.precio_base
        if self.asiento.tipo == 'primera':
            return precio_base * 2
        elif self.asiento.tipo == 'ejecutiva':
            return precio_base * 1.5
        return precio_base

class Boleto(models.Model):
    ESTADOS_BOLETO = [
        ('emitido', _('Emitido')),
        ('usado', _('Usado')),
        ('cancelado', _('Cancelado')),
    ]

    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, related_name='boleto', verbose_name=_('Reserva'))
    codigo_barra = models.CharField(_('Código de Barra'), max_length=50, unique=True)
    fecha_emision = models.DateTimeField(_('Fecha de Emisión'), auto_now_add=True)
    estado = models.CharField(_('Estado'), max_length=20, choices=ESTADOS_BOLETO, default='emitido')

    class Meta:
        verbose_name = _('Boleto')
        verbose_name_plural = _('Boletos')

    def __str__(self):
        return f"Boleto {self.codigo_barra}"

    def save(self, *args, **kwargs):
        if not self.codigo_barra:
            self.codigo_barra = str(uuid.uuid4())
        super().save(*args, **kwargs)
