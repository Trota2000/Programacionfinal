<<<<<<< HEAD
from django.shortcuts import render
from rest_framework import viewsets
from .models import Autor, Libro, Calificacion, Genero
from rest_framework.permissions import IsAuthenticated
from .serializers import AutorSerializer, LibroSerializer, CalificacionSerializer, GeneroSerializer
import matplotlib.pyplot as plt
import pandas as pd
from django.http import HttpResponse
from .models import Calificacion, Libro
from django.shortcuts import render

# ViewSet para Autor
class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [IsAuthenticated] 

# ViewSet para Libro
class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAuthenticated] 

# ViewSet para Calificación
class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated] 
    
    def get_queryset(self):
        # Solo devuelve las calificaciones del usuario autenticado
        user = self.request.user
        return Calificacion.objects.filter(user=user)

class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer
    permission_classes = [IsAuthenticated] 


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
=======
from django.shortcuts import render
from rest_framework import viewsets
from .models import Autor, Libro, Calificacion, Genero
from rest_framework.permissions import IsAuthenticated
from .serializers import AutorSerializer, LibroSerializer, CalificacionSerializer, GeneroSerializer
import matplotlib.pyplot as plt
import pandas as pd
from django.http import HttpResponse
from .models import Calificacion, Libro
from django.shortcuts import render

# ViewSet para Autor
class AutorViewSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    permission_classes = [IsAuthenticated] 

# ViewSet para Libro
class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAuthenticated] 

# ViewSet para Calificación
class CalificacionViewSet(viewsets.ModelViewSet):
    queryset = Calificacion.objects.all()
    serializer_class = CalificacionSerializer
    permission_classes = [IsAuthenticated] 
    
    def get_queryset(self):
        # Solo devuelve las calificaciones del usuario autenticado
        user = self.request.user
        return Calificacion.objects.filter(user=user)

class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializer
    permission_classes = [IsAuthenticated] 


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
>>>>>>> 6ad76b443f2bba257bc3796ff5374f13aaae8235
