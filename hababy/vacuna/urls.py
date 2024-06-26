from django.urls import path
from . import views

urlpatterns = [
    path('', views.vacunas, name='vacunas'),
    path('gripe/', views.vacuna, name='vacuna'),
    path('tos_ferina/', views.vacuna, name='vacuna'),
    path('gripe/eliminar_cita_vacuna/', views.eliminar_cita_vacuna, name='eliminar_cita_vacuna'),
    path('tos_ferina/eliminar_cita_vacuna/', views.eliminar_cita_vacuna, name='eliminar_cita_vacuna'),
   
]