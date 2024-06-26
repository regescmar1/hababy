from django.urls import path
from . import views


urlpatterns = [
    path('', views.extracciones, name='extracciones'),
    path('eliminar_cita_extracciones/', views.eliminar_cita_extracciones, name='eliminar_cita_extracciones'),
    path('test_o_sullivan_curva_larga/eliminar_cita_test_o_sullivan_curva_larga/', views.eliminar_cita_test_o_sullivan_curva_larga, name='eliminar_cita_test_o_sullivan_curva_larga'),
    path('test_o_sullivan_curva_larga/', views.test_o_sullivan_curva_larga, name='test_o_sullivan_curva_larga'),
    
    
]