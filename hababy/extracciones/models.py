from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import os

# Create your models here.



class CitaExtracciones(models.Model):
    usuaria=models.ForeignKey(User,on_delete=models.CASCADE)
    fecha=models.DateTimeField(null=True,blank=True)
    analisis_normal=models.BooleanField(null=True,blank=True,default=False)
    test_o_sullivan_positivo=models.BooleanField(null=True,blank=True,default=False)
    rh_negativo=models.BooleanField(null=True,blank=True,default=False)
    anemia=models.BooleanField(null=True,blank=True,default=False)
    observaciones=models.CharField(null=True,blank=True,max_length=255)
    trimestre=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])
   
class CurvaLarga(models.Model):
    usuaria=models.ForeignKey(User,on_delete=models.CASCADE)
    fecha=models.DateTimeField(null=True,blank=True)
    analisis_normal=models.BooleanField(null=True,blank=True,default=False)
    observaciones=models.CharField(null=True,blank=True,max_length=255)
    trimestre=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])