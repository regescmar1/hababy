from django.urls import path
from . import views



urlpatterns = [
    path('', views.gestion_citas, name='gestion_citas'),

    path('citas_primer/',views.citas_primer,name='citas_primer'),
    path('citas_segundo/',views.citas_segundo,name='citas_segundo'),
    path('citas_tercer/',views.citas_tercer,name='citas_tercer'),

]