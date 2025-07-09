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
- Configurar la base de datos:
En el archivo settings.py, configura la base de datos en PostgreSQL:
![base de datos](https://github.com/user-attachments/assets/07b54d6a-d26b-4cda-9ba3-eb1ff13ce117)
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
### 10. Ejecutar el servidor
Ejecuta el servidor para probar la aplicación:

```bash
python manage.py runserver

```
### 11. Probar la API con Postman

- Registrar un usuario:
![registrar usuarios](https://github.com/user-attachments/assets/4a65a82d-04cb-422c-b7f4-602fae0ca098)
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
- Consultar libros:

![consultar libros](https://github.com/user-attachments/assets/aaeac6f3-059a-4d23-aba5-4b1ff0785f01)
```bash
GET http://localhost:8000/api/libros/

```

- Insertar libro:
![insertar libros](https://github.com/user-attachments/assets/76fd3666-4c80-4180-84e3-b916dcdaf519)
```bash
POST http://127.0.0.1:8000/api/libros/crear/

```

```bash
{
    "nombre": "Libro de Prueba",
    "fecha_lanzamiento": "2023-01-01",
    "url_libro": "http://url-del-libro.com",
    "autor": 1,
    "genero": 2
}

```
- Eliminar libro:
![eliminar libros](https://github.com/user-attachments/assets/a78aba45-52b0-4e35-8b6e-5bec5c0a86b4)

```bash

```
```bash
DELETE http://127.0.0.1:8000/api/libros/1/eliminar/

```
Nota: Cambia el 1 en la URL por el ID del libro que deseas eliminar.

- Actualizar libro:
![modificar-actualizar libros](https://github.com/user-attachments/assets/17583110-fb7e-4b3a-8cc5-9926ff410166)

```bash
PUT http://127.0.0.1:8000/api/libros/1/actualizar/

```
```bash
{
    "nombre": "Libro de Prueba Modificado",
    "fecha_lanzamiento": "2023-02-01",
    "url_libro": "http://url-modificado.com",
    "autor": 2,
    "genero": 3
}

```
- Consultar autores:
![consultar autores](https://github.com/user-attachments/assets/1f892730-73d7-409c-b98e-0e4b18a8a10d)

```bash
GET http://127.0.0.1:8000/api/autores/

```
- Ingresar autor:
![insertar autores](https://github.com/user-attachments/assets/c8047993-395a-4829-898a-ac9d97df8310)

```bash
POST http://127.0.0.1:8000/api/autores/crear/

```

```bash
{
    "nombre": "Autor de Prueba",
    "nacionalidad": "Paraguaya"
}

```
- Consultar géneros:
![consultar generos](https://github.com/user-attachments/assets/fac5e7a5-31f6-4ead-8bd0-49a1b818aff5)

```bash
GET http://127.0.0.1:8000/api/generos/

```



## Documentación del analisis

Este script en Python está diseñado para realizar análisis sobre los registros y valoraciones dentro del sistema de la API Biblioteca. El propósito principal de este script es extraer datos de calificaciones y libros de la base de datos, procesarlos y generar gráficos que ayuden a comprender mejor la información almacenada.

### Funciones del Script

#### 1. `analizar_calificaciones(request)`

Esta función tiene como objetivo analizar las calificaciones de los libros realizadas por los usuarios. Extrae las calificaciones y los libros asociados, realiza un análisis de las calificaciones agrupadas por el año de publicación del libro, y genera un gráfico de barras.

```python
def analizar_calificaciones(request):
    try:
        # Obtener datos de calificaciones y libros
        calificaciones_data = Calificacion.objects.all().select_related('libro')
        libros_data = Libro.objects.all()

        # Convertir a DataFrame
        calificaciones_df = pd.DataFrame(list(calificaciones_data.values('libro', 'puntaje')))
        libros_df = pd.DataFrame(list(libros_data.values('id', 'nombre', 'autor', 'fecha_lanzamiento', 'genero')))

        # Filtrar las fechas fuera del rango válido
        libros_df['fecha_lanzamiento'] = pd.to_datetime(libros_df['fecha_lanzamiento'], errors='coerce')  # Convertir las fechas, invalidas se convertirán a NaT
        libros_df = libros_df.dropna(subset=['fecha_lanzamiento'])  # Eliminar las filas con fechas inválidas (NaT)

        # Merge de calificaciones y libros
        df = pd.merge(calificaciones_df, libros_df, left_on='libro', right_on='id')
        df['fecha_lanzamiento'] = pd.to_datetime(df['fecha_lanzamiento'])
        df['año_publicacion'] = df['fecha_lanzamiento'].dt.year

        # 1. Promedio de calificación por año de publicación
        promedio_por_ano = df.groupby('año_publicacion')['puntaje'].mean()

        # Crear gráfico del promedio de calificación por año de publicación
        plt.figure(figsize=(10, 6))
        promedio_por_ano.plot(kind='bar', color='skyblue')
        plt.title('Promedio de Calificación por Año de Publicación')
        plt.xlabel('Año de Publicación')
        plt.ylabel('Promedio de Calificación')

        # Guardar el gráfico como una imagen en memoria
        response = HttpResponse(content_type='image/png')
        plt.savefig(response, format='png')
        plt.close()

        return response

    except Exception as e:
        # Si ocurre un error, devolver el mensaje de error
        return HttpResponse(f"Error: {str(e)}", status=500)
```

#### 2. top_libros_calificados(request)
Esta función calcula y muestra los 5 libros mejor calificados por los usuarios. Para esto, agrupa los libros por el puntaje promedio de las calificaciones, ordenándolos de mayor a menor.

```python
def top_libros_calificados(request):
    try:
        # Obtener datos de calificaciones y libros
        calificaciones_data = Calificacion.objects.all().select_related('libro')
        libros_data = Libro.objects.all()

        # Convertir a DataFrame
        calificaciones_df = pd.DataFrame(list(calificaciones_data.values('libro', 'puntaje')))
        libros_df = pd.DataFrame(list(libros_data.values('id', 'nombre', 'autor', 'fecha_lanzamiento', 'genero')))

        # Merge de calificaciones y libros
        df = pd.merge(calificaciones_df, libros_df, left_on='libro', right_on='id')

        # Calcular el Top 5 libros mejor calificados
        top_libros = df.groupby('nombre')['puntaje'].mean().sort_values(ascending=False).head(5)

        # Crear gráfico del Top 5 libros mejor calificados
        plt.figure(figsize=(10, 6))
        top_libros.plot(kind='bar', color='orange')
        plt.title('Top 5 Libros Mejor Calificados')
        plt.xlabel('Libro')
        plt.ylabel('Promedio de Calificación')

        # Guardar el gráfico como una imagen en memoria
        response = HttpResponse(content_type='image/png')
        plt.savefig(response, format='png')
        plt.close()

        return response

    except Exception as e:
        # Si ocurre un error, devolver el mensaje de error
        return HttpResponse(f"Error: {str(e)}", status=500)


```
#### 3. cantidad_libros_por_genero(request)
Esta función muestra la cantidad de libros por género literario. Se agrupan los libros según su género y se genera un gráfico de barras que muestra la cantidad de libros por cada género.

```python

def cantidad_libros_por_genero(request):
    try:
        # Obtener datos de libros y géneros
        libros_data = Libro.objects.all().select_related('genero')  # Usamos select_related para obtener el nombre del género
        generos_data = Genero.objects.all()  # Obtener los géneros para usarlos en el gráfico

        # Convertir a DataFrame
        libros_df = pd.DataFrame(list(libros_data.values('id', 'nombre', 'autor', 'fecha_lanzamiento', 'genero')))
        generos_df = pd.DataFrame(list(generos_data.values('id', 'nombre')))  # Datos de géneros

        # Hacer un merge entre libros y géneros usando el id del género
        df = pd.merge(libros_df, generos_df, how='left', left_on='genero', right_on='id')

        # Renombrar las columnas para evitar conflictos
        df.rename(columns={'nombre_x': 'nombre_libro', 'nombre_y': 'nombre_genero'}, inplace=True)

        # Contar la cantidad de libros por género
        cantidad_por_genero = df.groupby('nombre_genero')['nombre_libro'].count().sort_values(ascending=False)

        # Crear gráfico de cantidad de libros por género
        plt.figure(figsize=(10, 6))
        cantidad_por_genero.plot(kind='bar', color='salmon')
        plt.title('Cantidad de Libros por Género')
        plt.xlabel('Género')
        plt.ylabel('Cantidad de Libros')

        # Guardar el gráfico como una imagen en memoria
        response = HttpResponse(content_type='image/png')
        plt.savefig(response, format='png')
        plt.close()

        return response

    except Exception as e:
        # Si ocurre un error, devolver el mensaje de error
        return HttpResponse(f"Error: {str(e)}", status=500)

```
### Generación y Explicación de Gráficos
Gráficos generados por el script:
- Promedio de Calificación por Año de Publicación:

Gráfico de barras que muestra el promedio de las calificaciones de los libros agrupados por año de publicación. Este gráfico es útil para ver cómo han sido calificados los libros a lo largo de los años.

![promedio de calificacion](https://github.com/user-attachments/assets/59e793f1-0f70-42bc-bb1b-fbca8bd62e0c)

Eje X: Año de publicación de los libros.

Eje Y: Promedio de las calificaciones.

- Top 5 Libros Mejor Calificados:

Gráfico de barras que muestra los 5 libros mejor calificados. Este gráfico permite identificar rápidamente cuáles son los libros más populares en función de las valoraciones de los usuarios.

![top 5 mejores](https://github.com/user-attachments/assets/629aa5c7-98ea-4b47-86b0-87b2c8cf8b8f)

Eje X: Nombres de los libros.

Eje Y: Promedio de calificación de cada libro.

- Cantidad de Libros por Género:

Gráfico de barras que muestra la cantidad de libros registrados en cada género literario. Este gráfico es útil para ver qué géneros tienen más libros disponibles en la biblioteca.

![Cantidad de libros por genero](https://github.com/user-attachments/assets/23737f52-0061-4739-b8b1-54eaefeff839)

Eje X: Géneros literarios.

Eje Y: Número de libros en cada género.

Cada gráfico es generado utilizando Matplotlib y los datos se manipulan con Pandas. Los gráficos se guardan como imágenes en formato PNG y se devuelven al usuario en la respuesta HTTP.











