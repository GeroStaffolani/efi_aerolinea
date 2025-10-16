from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Avion, Vuelo, Pasajero, Asiento, Reserva, Boleto
from datetime import datetime, timedelta, date
from decimal import Decimal


class AvionAPITests(APITestCase):
    # Tests para el endpoint de Aviones
    
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', 'adminpass')
        self.regular_user = User.objects.create_user('user', 'user@test.com', 'userpass')
        
        # Obtener token JWT para admin
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(self.admin)
        self.admin_token = str(refresh.access_token)
        
        # Token para usuario regular
        refresh_user = RefreshToken.for_user(self.regular_user)
        self.user_token = str(refresh_user.access_token)
        
        self.avion_data = {
            'modelo': 'Boeing 737',
            'capacidad': 100,
            'filas': 20,
            'columnas': 5,
            'activo': True
        }

    def test_create_avion_as_admin(self):
        # Test crear avión como administrador
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        url = reverse('avion-list')
        response = self.client.post(url, self.avion_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Avion.objects.count(), 1)
        self.assertEqual(Avion.objects.get().modelo, 'Boeing 737')

    def test_create_avion_as_regular_user_forbidden(self):
        # Test que usuario no admin no puede crear avión
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        url = reverse('avion-list')
        response = self.client.post(url, self.avion_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_aviones(self):
        # Test listar aviones
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        Avion.objects.create(**self.avion_data)
        url = reverse('avion-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_update_avion_as_admin(self):
        # Test editar avión como administrador
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        avion = Avion.objects.create(**self.avion_data)
        url = reverse('avion-detail', kwargs={'pk': avion.id})
        updated_data = {'modelo': 'Airbus A320', 'capacidad': 150, 'filas': 25, 'columnas': 6, 'activo': True}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        avion.refresh_from_db()
        self.assertEqual(avion.modelo, 'Airbus A320')


class PasajeroAPITests(APITestCase):
    # Tests para el endpoint de Pasajeros
    
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@test.com', 'userpass')
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(self.user)
        self.user_token = str(refresh.access_token)
        
        self.pasajero_data = {
            'nombre': 'Juan Pérez',
            'documento': '12345678',
            'tipo_documento': 'dni',
            'email': 'juan@email.com',
            'telefono': '123456789',
            'fecha_nacimiento': '1990-01-01'
        }

    def test_create_pasajero(self):
        # Test crear pasajero
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        url = reverse('pasajero-list')
        response = self.client.post(url, self.pasajero_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pasajero.objects.count(), 1)
        self.assertEqual(Pasajero.objects.get().nombre, 'Juan Pérez')

    def test_create_pasajero_future_birth_date_invalid(self):
        # Test que no se puede crear pasajero con fecha de nacimiento futura
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        invalid_data = self.pasajero_data.copy()
        invalid_data['fecha_nacimiento'] = '2030-01-01'  # Fecha futura
        
        url = reverse('pasajero-list')
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_pasajeros(self):
        # Test listar pasajeros
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        Pasajero.objects.create(**self.pasajero_data)
        
        url = reverse('pasajero-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)


class AuthenticationTests(APITestCase):
    # Tests para autenticación JWT
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@test.com', 'testpass123')

    def test_get_token_success(self):
        # Test obtener token JWT con credenciales válidas
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_get_token_invalid_credentials(self):
        # Test obtener token con credenciales inválidas
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_endpoint_without_token(self):
        # Test acceder a endpoint protegido sin token
        url = reverse('avion-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_endpoint_with_valid_token(self):
        # Test acceder a endpoint protegido con token válido
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(self.user)
        token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        url = reverse('avion-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
