# 🛩️ EFI Aerolínea - Sistema de Gestión de Vuelos

Sistema integral de gestión de aerolínea desarrollado con Django y Django REST Framework (DRF) que permite la gestión completa de vuelos, pasajeros, reservas y boletos. Incluye tanto una interfaz web tradicional como una API REST completa para integración con terceros.

## 🚀 Características Principales

### 🌐 Aplicación Web
- **Búsqueda y reserva de vuelos** con filtros avanzados
- **Gestión de pasajeros** y perfiles de usuario
- **Sistema de reservas** con selección de asientos
- **Panel de administración** completo
- **Reportes** de vuelos y pasajeros
- **Interfaz responsive** adaptable a dispositivos móviles
- **Soporte multilenguaje** (Español/Inglés)

### 🔗 API REST
- **Endpoints RESTful** para todas las funcionalidades
- **Autenticación JWT** para acceso seguro
- **Documentación automática** with Swagger/ReDoc
- **Serializers** con validaciones robustas
- **Permisos granulares** por roles de usuario
- **Manejo de errores** HTTP estandarizado

## 📋 Tecnologías Utilizadas

- **Backend:** Django 4.2.7, Django REST Framework 3.14.0
- **Base de Datos:** SQLite3 (configurable a PostgreSQL/MySQL)
- **Autenticación:** JWT (djangorestframework-simplejwt)
- **Documentación API:** drf-yasg (Swagger/ReDoc)
- **Frontend:** HTML5, CSS3, Bootstrap
- **Imágenes:** Pillow para manejo de archivos
- **Configuración:** python-decouple

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- pip
- Git

### Pasos de Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/GeroStaffolani/efi_aerolinea.git
   cd efi_aerolinea
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crear superusuario:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Crear datos de ejemplo (opcional):**
   ```bash
   python scripts/create_sample_data.py
   ```

7. **Ejecutar servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

## 🌐 URLs y Acceso

### Aplicación Web
- **Home:** http://127.0.0.1:8000/
- **Buscar Vuelos:** http://127.0.0.1:8000/buscar/
- **Mis Reservas:** http://127.0.0.1:8000/mis-reservas/
- **Admin Django:** http://127.0.0.1:8000/admin/

### API REST Endpoints

#### 🔐 Autenticación
- **Obtener Token:** `POST /api/token/`
- **Refresh Token:** `POST /api/token/refresh/`

#### ✈️ Gestión de Vuelos
- **Listar vuelos:** `GET /vuelos/`
- **Crear vuelo:** `POST /vuelos/` (solo admin)
- **Detalle vuelo:** `GET /vuelos/{id}/`
- **Actualizar vuelo:** `PUT/PATCH /vuelos/{id}/` (solo admin)
- **Eliminar vuelo:** `DELETE /vuelos/{id}/` (solo admin)
- **Asientos disponibles:** `GET /vuelos/{id}/asientos_disponibles/`

#### 🛫 Gestión de Aviones
- **Listar aviones:** `GET /aviones/`
- **Crear avión:** `POST /aviones/` (solo admin)
- **Detalle avión:** `GET /aviones/{id}/`
- **Actualizar avión:** `PUT/PATCH /aviones/{id}/` (solo admin)
- **Eliminar avión:** `DELETE /aviones/{id}/` (solo admin)

#### 👥 Gestión de Pasajeros
- **Listar pasajeros:** `GET /pasajeros/`
- **Registrar pasajero:** `POST /pasajeros/`
- **Detalle pasajero:** `GET /pasajeros/{id}/`
- **Actualizar pasajero:** `PUT/PATCH /pasajeros/{id}/`
- **Eliminar pasajero:** `DELETE /pasajeros/{id}/`

#### 💺 Gestión de Asientos
- **Listar asientos:** `GET /asientos/`
- **Crear asiento:** `POST /asientos/` (solo admin)
- **Detalle asiento:** `GET /asientos/{id}/`
- **Actualizar asiento:** `PUT/PATCH /asientos/{id}/` (solo admin)
- **Eliminar asiento:** `DELETE /asientos/{id}/` (solo admin)

#### 📝 Sistema de Reservas
- **Listar reservas:** `GET /reservas/`
- **Crear reserva:** `POST /reservas/`
- **Detalle reserva:** `GET /reservas/{id}/`
- **Actualizar reserva:** `PUT/PATCH /reservas/{id}/`
- **Cancelar reserva:** `DELETE /reservas/{id}/`

#### 🎫 Gestión de Boletos
- **Listar boletos:** `GET /boletos/`
- **Crear boleto:** `POST /boletos/`
- **Detalle boleto:** `GET /boletos/{id}/`
- **Actualizar boleto:** `PUT/PATCH /boletos/{id}/`
- **Eliminar boleto:** `DELETE /boletos/{id}/`

### 📖 Documentación de API
- **Swagger UI:** http://127.0.0.1:8000/swagger/
- **ReDoc:** http://127.0.0.1:8000/redoc/

## 🏗️ Estructura del Proyecto

```
efi_aerolinea/
├── airline_system/           # Configuración principal Django
│   ├── __init__.py
│   ├── settings.py          # Configuración del proyecto
│   ├── urls.py              # URLs principales y API
│   └── wsgi.py
│
├── flights/                 # Aplicación principal
│   ├── __init__.py
│   ├── admin.py            # Configuración admin Django
│   ├── models.py           # Modelos de datos
│   ├── serializers.py      # Serializers DRF
│   ├── views.py            # Vistas web y API ViewSets
│   ├── urls.py             # URLs de la app
│   ├── services.py         # Lógica de negocio
│   ├── permissions.py      # Permisos personalizados
│   ├── forms.py            # Formularios Django
│   ├── tests.py            # Tests unitarios
│   ├── context_processors.py
│   └── templatetags/
│       └── flight_extras.py
│
├── templates/              # Plantillas HTML
│   ├── base.html
│   ├── flights/
│   └── registration/
│
├── locale/                 # Archivos de traducción
│   ├── en/LC_MESSAGES/
│   └── es/LC_MESSAGES/
│
├── scripts/                # Scripts de utilidades
│   └── create_sample_data.py
│
├── static/                 # Archivos estáticos
├── media/                  # Archivos subidos
├── requirements.txt        # Dependencias Python
├── manage.py              # Script de gestión Django
└── README.md              # Este archivo
```

## 🗄️ Modelos de Datos

### Avión
- **modelo:** Nombre del modelo del avión
- **capacidad:** Número total de asientos
- **filas/columnas:** Configuración de layout
- **activo:** Estado del avión

### Vuelo
- **avion:** Relación con modelo Avión
- **codigo_vuelo:** Código único del vuelo
- **origen/destino:** Ciudades de origen y destino
- **fecha_salida/llegada:** Fechas y horarios
- **estado:** Estado actual del vuelo
- **precio_base:** Precio base del boleto

### Pasajero
- **nombre:** Nombre completo
- **documento:** Número de documento único
- **tipo_documento:** DNI, Pasaporte, Cédula
- **email/telefono:** Información de contacto
- **fecha_nacimiento:** Fecha de nacimiento

### Asiento
- **avion:** Relación con Avión
- **numero:** Identificador del asiento (ej: 12A)
- **fila/columna:** Posición en el avión
- **tipo:** Primera, Ejecutiva, Económica
- **estado:** Disponible, Reservado, Ocupado

### Reserva
- **vuelo/pasajero/asiento:** Relaciones principales
- **estado:** Pendiente, Confirmada, Cancelada
- **fecha_reserva:** Timestamp de creación
- **precio_total:** Precio final de la reserva

### Boleto
- **reserva:** Relación con Reserva
- **codigo_boleto:** Código único del boleto
- **fecha_emision:** Fecha de emisión
- **estado:** Activo, Usado, Cancelado

## 🔐 Autenticación y Permisos

### Sistema de Autenticación
- **JWT Tokens** para autenticación API
- **Session Authentication** para interfaz web
- **Tokens de acceso** con duración de 30 minutos
- **Refresh tokens** con duración de 1 día

### Permisos por Endpoint
- **Público:** Consulta de vuelos disponibles
- **Autenticado:** Gestión de reservas propias
- **Administrador:** CRUD completo de vuelos y aviones

## 🧪 Testing

### Ejecutar Tests
```bash
python manage.py test
```

### Estructura de Tests
- **tests.py:** Tests unitarios para API endpoints
- **Cobertura:** Funcionalidades básicas de CRUD
- **Autenticación:** Tests de JWT y permisos

## 🔧 Configuración Avanzada

### Variables de Entorno
Crear archivo `.env` para configuración:
```env
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Base de Datos PostgreSQL
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'efi_aerolinea',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📚 Uso de la API

### Ejemplo: Obtener Token
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "tu_password"}'
```

### Ejemplo: Crear Pasajero
```bash
curl -X POST http://127.0.0.1:8000/pasajeros/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer tu_token_aqui" \
  -d '{
    "nombre": "Juan Pérez",
    "documento": "12345678",
    "tipo_documento": "dni",
    "email": "juan@email.com",
    "telefono": "123456789",
    "fecha_nacimiento": "1990-01-01"
  }'
```

### Ejemplo: Buscar Vuelos
```bash
curl -X GET "http://127.0.0.1:8000/vuelos/?origen=Buenos Aires&destino=Madrid" \
  -H "Authorization: Bearer tu_token_aqui"
```

