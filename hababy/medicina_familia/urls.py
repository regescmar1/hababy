from django.urls import path
from . import views


urlpatterns = [
    path('acido_folico/',views.acido_folico, name='acido_folico'),
    path('hierro/',views.hierro, name='hierro'),
    path('acido_folico/eliminar_cita_medicina_familia/', views.eliminar_cita_medicina_familia, name='eliminar_cita_medicina_familia'),
    path('hierro/eliminar_cita_medicina_familia/', views.eliminar_cita_medicina_familia, name='eliminar_cita_medicina_familia'),
   
]