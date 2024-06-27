from django.urls import path
from . import views

urlpatterns = [
    path('', views.administrador, name='administrador'),
    path('gestion_usuarias/', views.gestion_usuarias, name='gestion_usuarias'),
    path('gestion_usuarias/usuaria/<int:usuaria_id>/', views.usuaria, name='usuaria'),
    path('perfil_actualizado_admin/',views.perfil_actualizado_admin,name="perfil_actualizado_admin"),
    path('gestion_usuarias/usuaria/<int:usuaria_id>/eliminar/', views.eliminar_usuaria, name='eliminar_usuaria'),
    path('gestion_usuarias/usuaria/crear/', views.crear_usuaria, name='crear_usuaria'),
    path('citas/', views.citas, name='citas'),
    path('gestion_extracciones/', views.gestion_extracciones, name='gestion_extracciones'),
    path('gestion_vacunas/', views.gestion_vacunas, name='gestion_vacunas'),
    path('gestion_odontologia/', views.gestion_odontologia, name='gestion_odontologia'),
]
