# GroPott Air - Sistema de Aerolínea

GroPott Air es una aplicación web desarrollada con Django para la gestión integral de vuelos, reservas y pasajeros de una aerolínea. El sistema permite a los usuarios buscar vuelos, realizar reservas, gestionar asientos y acceder a reportes administrativos, todo desde una interfaz moderna y responsiva.

## Características principales
- Registro e inicio de sesión de usuarios
- Panel de administración para staff
- Búsqueda y reserva de vuelos
- Gestión de pasajeros y asientos
- Estadísticas y reportes
- Interfaz profesional y adaptable a dispositivos móviles
- Soporte multilenguaje (Español/Inglés)

## Instalación
1. Clona el repositorio:
   ```
   git clone <URL-del-repositorio>
   ```
2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
3. Aplica migraciones:
   ```
   python manage.py migrate
   ```
4. Crea datos de ejemplo:
   ```
   python scripts/create_sample_data.py
   ```
5. Ejecuta el servidor:
   ```
   python manage.py runserver
   ```

## Acceso rápido
- Panel de administración: `/admin/`
- Usuario admin por defecto: `admin` / `admin123`

## Estructura del proyecto
```
EFI/
├── airline_system/         # Configuración principal de Django
│   ├── __init__.py
│   ├── settings.py         # Configuración del proyecto
│   ├── urls.py             # Rutas principales
│   └── wsgi.py
│
├── flights/                # App principal: lógica, modelos, vistas
│   ├── __init__.py
│   ├── admin.py            # Configuración del admin
│   ├── context_processors.py
│   ├── forms.py            # Formularios personalizados
│   ├── models.py           # Modelos de datos
│   ├── services.py         # Lógica de negocio
│   ├── urls.py             # Rutas de la app
│   ├── views.py            # Vistas
│   └── templatetags/
│       └── flight_extras.py
│
├── scripts/
│   └── create_sample_data.py # Script para datos de ejemplo
│
├── templates/
│   ├── base.html           # Template base
│   ├── flights/            # Templates de la app
│   │   ├── home.html
│   │   ├── buscar_vuelos.html
│   │   ├── crear_reserva.html
│   │   ├── detalle_reserva.html
│   │   ├── detalle_vuelo.html
│   │   ├── mis_reservas.html
│   │   ├── reporte_pasajeros_vuelo.html
│   │   └── reportes.html
│   └── registration/       # Login y registro
│       ├── login.html
│       └── registro.html
│
├── locale/                 # Archivos de traducción
│   ├── en/LC_MESSAGES/
│   │   ├── django.po
│   │   └── django.mo
│   └── es/LC_MESSAGES/
│       ├── django.po
│       └── django.mo
│
├── requirements.txt        # Dependencias
├── manage.py               # Comando principal de Django
├── db.sqlite3              # Base de datos SQLite
└── README.md               # Este archivo
```

## Personalización
- Modifica los estilos globales en `templates/base.html`.
- Personaliza los templates en `templates/flights/` y `templates/registration/`.
- Agrega nuevos idiomas en la carpeta `locale/`.

## Licencia
Este proyecto es solo para fines educativos y de demostración.

---

