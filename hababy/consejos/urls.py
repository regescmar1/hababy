from django.urls import path
from . import views

urlpatterns = [
    path('', views.consejos, name='consejos'),
    path('nauseas/', views.nauseas, name='nauseas'),
    path('ejercicios/', views.ejercicios, name='ejercicios'),
    path('nutricion/', views.nutricion, name='nutricion'),
    path('lactancia/', views.lactancia, name='lactancia'),
    path('bolso_hospital/', views.bolso_hospital, name='bolso_hospital'),
    path('contracciones/', views.contracciones, name='contracciones'),
    path('induccion_al_parto/', views.induccion_al_parto, name='induccion_al_parto'),
    path('cordon_umbilical/', views.cordon_umbilical, name='cordon_umbilical'),
    path('suelo_pelvico/', views.suelo_pelvico, name='suelo_pelvico'),
]