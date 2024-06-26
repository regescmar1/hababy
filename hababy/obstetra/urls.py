from django.urls import path
from . import views

urlpatterns = [
    path('', views.obstetra, name='obstetra'),
    path('eliminar_cita_obstetra/', views.eliminar_cita_obstetra, name='eliminar_cita_obstetra'),
    path('eliminar_cita_obstetra/uno/', views.eliminar_cita_obstetra, name='eliminar_cita_obstetra'),
    path('eliminar_cita_obstetra/dos/', views.eliminar_cita_obstetra, name='eliminar_cita_obstetra'),
    path('eliminar_cita_obstetra/tres/', views.eliminar_cita_obstetra, name='eliminar_cita_obstetra'),
    path('uno/', views.obstetra, name='obstetra'),
    path('dos/', views.obstetra, name='obstetra'),
    path('tres/', views.obstetra, name='obstetra'),
]