from django.urls import path
from . import views

urlpatterns = [
    path('',views.proxima_cita,name='proxima_cita'),
]