from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Avion

class AvionAPITests(APITestCase):
    """Tests básicos para el endpoint de Aviones"""
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', 'adminpass')
        # Obtener token JWT
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(self.admin)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.avion_data = {
            'modelo': 'Boeing 737',
            'capacidad': 100,
            'filas': 20,
            'columnas': 5,
            'activo': True
        }

    def test_create_avion(self):
        url = reverse('avion-list')
        response = self.client.post(url, self.avion_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Avion.objects.count(), 1)
        self.assertEqual(Avion.objects.get().modelo, 'Boeing 737')

    def test_list_aviones(self):
        Avion.objects.create(**self.avion_data)
        url = reverse('avion-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)
