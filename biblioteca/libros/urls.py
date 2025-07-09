<<<<<<< HEAD
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AutorViewSet, GeneroViewSet, LibroViewSet, CalificacionViewSet
from . import views


router = DefaultRouter()
router.register(r'autores', AutorViewSet)
router.register(r'libros', LibroViewSet)
router.register(r'calificaciones', CalificacionViewSet)
router.register(r'generos', GeneroViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('analizar/calificaciones/', views.analizar_calificaciones, name='analizar_calificaciones'),
    path('analizar/top-libros-calificados/', views.top_libros_calificados, name='top_libros_calificados'),
    path('analizar/cantidad-libros-por-genero/', views.cantidad_libros_por_genero, name='cantidad_libros_por_genero'),

]

=======
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AutorViewSet, GeneroViewSet, LibroViewSet, CalificacionViewSet
from . import views


router = DefaultRouter()
router.register(r'autores', AutorViewSet)
router.register(r'libros', LibroViewSet)
router.register(r'calificaciones', CalificacionViewSet)
router.register(r'generos', GeneroViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('analizar/calificaciones/', views.analizar_calificaciones, name='analizar_calificaciones'),
    path('analizar/top-libros-calificados/', views.top_libros_calificados, name='top_libros_calificados'),
    path('analizar/cantidad-libros-por-genero/', views.cantidad_libros_por_genero, name='cantidad_libros_por_genero'),

]

>>>>>>> 6ad76b443f2bba257bc3796ff5374f13aaae8235
