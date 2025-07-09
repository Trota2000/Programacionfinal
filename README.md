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




