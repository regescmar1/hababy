# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class CitaMatronaComunObstetra(models.Model):
    usuaria=models.ForeignKey(User,on_delete=models.CASCADE)
    fecha=models.DateTimeField(null=True,blank=True)
    peso=models.FloatField(null=True,blank=True,validators=[MinValueValidator(0.0), MaxValueValidator(200.0)])
    altura=models.FloatField(null=True,blank=True,validators=[MinValueValidator(0.0), MaxValueValidator(2.0)])
    imc=models.FloatField(null=True,blank=True)
    tas=models.IntegerField(null=True,blank=True,validators=[MinValueValidator(0), MaxValueValidator(300)])
    tad=models.IntegerField(null=True,blank=True,validators=[MinValueValidator(0), MaxValueValidator(200)])
    trimestre=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])
    orden=models.IntegerField(null=True,blank=True,validators=[MinValueValidator(1), MaxValueValidator(2)])
    class Meta:
        abstract = True



class CitaMatrona(CitaMatronaComunObstetra):
    #2º trimestre orden 2 y 3er trimestre orden 1 y 2
    exploracion_obstetrica=models.CharField(null=True,blank=True,max_length=255)
    #3er trimestre orden 2
    egb=models.BooleanField(null=True,blank=True,default=False)

    