from django.db import models
from matrona.models import CitaMatronaComunObstetra
# Create your models here.
class CitaObstetra(CitaMatronaComunObstetra):
    observaciones=models.CharField(null=True,blank=True,max_length=255)
    #40semanas
    monitores=models.CharField(null=True,blank=True,max_length=255)