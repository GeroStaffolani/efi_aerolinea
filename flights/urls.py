from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views

# DRF router para los endpoints API
router = DefaultRouter()
router.register(r'aviones', views.AvionViewSet)
router.register(r'vuelos', views.VueloViewSet)
router.register(r'pasajeros', views.PasajeroViewSet)
router.register(r'asientos', views.AsientoViewSet)
router.register(r'reservas', views.ReservaViewSet)
router.register(r'boletos', views.BoletoViewSet)

urlpatterns = [
    # Páginas principales
    path('', views.home, name='home'),
    path('buscar/', views.buscar_vuelos, name='buscar_vuelos'),
    path('vuelo/<int:vuelo_id>/', views.detalle_vuelo, name='detalle_vuelo'),
    
    # Reservas
    path('reservar/<int:vuelo_id>/', views.crear_reserva, name='crear_reserva'),
    path('reserva/<int:reserva_id>/', views.detalle_reserva, name='detalle_reserva'),
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('cancelar-reserva/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    
    # Reportes
    path('reportes/', views.reportes, name='reportes'),
    path('reportes/vuelo/<int:vuelo_id>/pasajeros/', views.reporte_pasajeros_vuelo, name='reporte_pasajeros_vuelo'),
    
    # AJAX
    path('ajax/asientos/<int:vuelo_id>/', views.obtener_asientos_ajax, name='obtener_asientos_ajax'),
    path('ajax/ciudades/', views.obtener_ciudades_ajax, name='obtener_ciudades_ajax'),
    path('ajax/sugerencias-viajes/', views.obtener_sugerencias_viajes_ajax, name='obtener_sugerencias_viajes_ajax'),
    
    # Autenticación
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
    # Endpoints API REST
    path('api/', include(router.urls)),
]
