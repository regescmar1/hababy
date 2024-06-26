from django.urls import path
from . import views


urlpatterns = [
    path('', views.odontologia, name='odontologia'),
    path('eliminar_cita_odontologia/', views.eliminar_cita_odontologia, name='eliminar_cita_odontologia'),
]