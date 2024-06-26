from django.urls import path
from . import views

urlpatterns = [
    path('', views.matrona, name='matrona'),
    path('eliminar_cita_matrona/', views.eliminar_cita_matrona, name='eliminar_cita_matrona'),
    path('eliminar_cita_matrona/uno/', views.eliminar_cita_matrona, name='eliminar_cita_matrona'),
    path('eliminar_cita_matrona/dos/', views.eliminar_cita_matrona, name='eliminar_cita_matrona'),
    path('uno/', views.matrona, name='matrona'),
    path('dos/', views.matrona, name='matrona'),
]