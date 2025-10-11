
from rest_framework import serializers
from .models import Avion, Vuelo, Pasajero, Asiento, Reserva, Boleto

class AvionSerializer(serializers.ModelSerializer):
	def validate(self, data):
		if data.get('filas', 1) < 1 or data.get('columnas', 1) < 1:
			raise serializers.ValidationError('El avión debe tener al menos 1 fila y 1 columna.')
		if data.get('capacidad', 1) < 1:
			raise serializers.ValidationError('La capacidad debe ser mayor a 0.')
		return data
	class Meta:
		model = Avion
		fields = '__all__'

class VueloSerializer(serializers.ModelSerializer):
	def validate(self, data):
		if data['fecha_llegada'] <= data['fecha_salida']:
			raise serializers.ValidationError('La fecha de llegada debe ser posterior a la de salida.')
		if data['precio_base'] <= 0:
			raise serializers.ValidationError('El precio base debe ser mayor a 0.')
		return data
	avion = AvionSerializer(read_only=True)
	avion_id = serializers.PrimaryKeyRelatedField(queryset=Avion.objects.all(), source='avion', write_only=True)
	class Meta:
		model = Vuelo
		fields = '__all__'

class PasajeroSerializer(serializers.ModelSerializer):
	def validate(self, data):
		if data['fecha_nacimiento'] >= serializers.DateField().to_internal_value(str(serializers.DateField().to_representation(serializers.DateField().to_internal_value('today')))):
			raise serializers.ValidationError('La fecha de nacimiento debe ser en el pasado.')
		return data
	class Meta:
		model = Pasajero
		fields = '__all__'

class AsientoSerializer(serializers.ModelSerializer):
	def validate(self, data):
		if data['fila'] < 1:
			raise serializers.ValidationError('La fila debe ser mayor a 0.')
		return data
	avion = AvionSerializer(read_only=True)
	avion_id = serializers.PrimaryKeyRelatedField(queryset=Avion.objects.all(), source='avion', write_only=True)
	class Meta:
		model = Asiento
		fields = '__all__'

class ReservaSerializer(serializers.ModelSerializer):
	def validate(self, data):
		# Validar que el asiento pertenezca al avión del vuelo
		vuelo = data.get('vuelo')
		asiento = data.get('asiento')
		if vuelo and asiento and asiento.avion_id != vuelo.avion_id:
			raise serializers.ValidationError('El asiento no pertenece al avión de este vuelo.')
		return data
	vuelo = VueloSerializer(read_only=True)
	vuelo_id = serializers.PrimaryKeyRelatedField(queryset=Vuelo.objects.all(), source='vuelo', write_only=True)
	pasajero = PasajeroSerializer(read_only=True)
	pasajero_id = serializers.PrimaryKeyRelatedField(queryset=Pasajero.objects.all(), source='pasajero', write_only=True)
	asiento = AsientoSerializer(read_only=True)
	asiento_id = serializers.PrimaryKeyRelatedField(queryset=Asiento.objects.all(), source='asiento', write_only=True)
	class Meta:
		model = Reserva
		fields = '__all__'

class BoletoSerializer(serializers.ModelSerializer):
	reserva = ReservaSerializer(read_only=True)
	reserva_id = serializers.PrimaryKeyRelatedField(queryset=Reserva.objects.all(), source='reserva', write_only=True)
	class Meta:
		model = Boleto
		fields = '__all__'
