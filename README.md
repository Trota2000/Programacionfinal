# Proyecto de API Biblioteca - Diego Troche

## Descripción del Proyecto

Este proyecto es una API RESTful desarrollada con **Django** y **Django REST Framework** para gestionar una biblioteca. La aplicación permite manejar libros, autores, géneros literarios y calificaciones por parte de los usuarios. Además, incluye funciones para registrar usuarios, calificar libros y visualizar estadísticas relacionadas con las calificaciones y libros.

## Pasos para crear el proyecto

### 1. Crear una carpeta para el proyecto

Primero, crea una carpeta para tu proyecto. Puedes llamarla **Biblioteca** o el nombre que prefieras.

```bash
mkdir Biblioteca
cd Biblioteca
```
### 2. Crear un entorno virtual
Entra en la carpeta del proyecto y crea un entorno virtual con el siguiente comando:
```bash
python -m venv venv
```
### 3. Activar el entorno virtual
Una vez creado el entorno virtual, actívalo con:

Windows:
```bash
.\venv\Scripts\activate
```

### 4. Instalar las librerías necesarias

Con el entorno activado, instala las librerías necesarias utilizando el siguiente bloque de comandos:

```bash
# Instalar Django 4.2
pip install django==4.2  # Framework principal para el desarrollo web.

# Instalar psycopg2-binary
pip install psycopg2-binary  # Driver para conectar Django con bases de datos PostgreSQL.

# Instalar Django Rest Framework
pip install djangorestframework  # Proporciona herramientas para construir APIs RESTful en Django.

# Instalar Simple JWT
pip install djangorestframework-simplejwt  # Proporciona autenticación con tokens JWT para la API.
```
### 5. Crear el proyecto Django
Con las librerías instaladas, crea el proyecto Django con el siguiente comando:

```bash
django-admin startproject biblioteca
```
### 6. Configurar el proyecto
Configurar Rest Framework:
Abre settings.py dentro de la carpeta biblioteca y agrega las siguientes líneas a INSTALLED_APPS:

```bash
'rest_framework',
'rest_framework_simplejwt',
```
Configurar la base de datos:
En el archivo settings.py, configura la base de datos en PostgreSQL:
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'biblioteca',
        'USER': 'postgres',
        'PASSWORD': 'tu_contrasenha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

```

Configurar Rest Framework en settings.py:
Añade la configuración de JWT Authentication en settings.py:
```bash
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=8),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ("Bearer",),
}

```

Asegúrate de importar timedelta en el archivo settings.py:

```bash
from datetime import timedelta

```
### 7. Crear las aplicaciones de Django
Entra a la carpeta del proyecto y crea las aplicaciones necesarias:

```bash
cd biblioteca
django-admin startapp accounts
django-admin startapp libros
```
### 8. Configurar las aplicaciones
App accounts
Crear serializers.py:

En la carpeta accounts, crea un archivo serializers.py con el siguiente código:

```bash
from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

```
- Crear views.py:

En views.py de la aplicación accounts, crea la vista de registro de usuario:


```bash
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.permissions import AllowAny

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

```
- Crear urls.py:

En la carpeta accounts, crea un archivo urls.py con el siguiente código:

```bash
from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

```

- Modificar urls.py en biblioteca:

En el archivo biblioteca/urls.py, agrega la URL de accounts:

```bash
from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('accounts.urls')),
    # otras rutas...
]

```
- App libros
Crear models.py:

En la carpeta libros, crea el archivo models.py con el siguiente código:
```bash
from django.db import models
from django.contrib.auth.models import User

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Genero(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre
    
class Libro(models.Model):
    nombre = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    fecha_lanzamiento = models.DateField()
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, related_name='libros')
    url_libro = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Calificacion(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='calificaciones')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    puntaje = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.libro.nombre}: {self.puntaje}"

```
- Crear views.py:

En views.py de la app libros, crea las vistas de los libros y calificaciones:

```bash
from django.shortcuts import render
from rest_framework import viewsets
from .models import Autor, Libro, Calificacion, Genero
from rest_framework.permissions import IsAuthenticated
from .serializers import AutorSerializer, LibroSerializer, CalificacionSerializer, GeneroSerializer

class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [IsAuthenticated]

class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAuthenticated]

class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Calificacion.objects.filter(user=user)

class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer
    permission_classes = [IsAuthenticated]

```
- Crear urls.py:

En la carpeta libros, crea un archivo urls.py con el siguiente código:

```bash
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AutorViewSet, LibroViewSet, CalificacionViewSet

router = DefaultRouter()
router.register(r'autores', AutorViewSet)
router.register(r'libros', LibroViewSet)
router.register(r'calificaciones', CalificacionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

```
- Modificar biblioteca/urls.py:

Agrega las rutas para las vistas de libros:

```bash
from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('accounts.urls')),
    path('api/libros/', include('libros.urls')),
]

```

### 9. Realizar las migraciones
Realiza las migraciones para crear las tablas en la base de datos:

```bash
python manage.py makemigrations
python manage.py migrate

```
10. Ejecutar el servidor
Ejecuta el servidor para probar la aplicación:

```bash
python manage.py runserver

```
### 11. Probar la API con Postman

- Registrar un usuario:

```bash
POST http://127.0.0.1:8000/api/auth/register/

```
```bash
{
    "username": "DiegoTroche",
    "password": "123456",
    "email": "diegotroche2000@gmail.com"
}

```
- Iniciar sesión:
```bash
POST http://127.0.0.1:8000/api/auth/login/

```|

```bash
{
    "username": "DiegoTroche",
    "password": "123456"
}

```

```bash
GET http://localhost:8000/api/libros/

```




