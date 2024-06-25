from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.educacion_maternal, name='educacion_maternal'),
    path('sesion/crear/', views.crear_sesion, name='crear_sesion'),
    path('sesion/<int:sesion_id>/', views.sesion, name='sesion'),
    path('sesion/<int:sesion_id>/eliminar/', views.eliminar_sesion, name='eliminar_sesion'),
]