
from django.db import models
from django.contrib.auth.models import User
from extracciones.models import CitaExtracciones, CurvaLarga
from obstetra.models import CitaObstetra


class ArchivoExtracciones(models.Model):
    usuaria=models.ForeignKey(User,on_delete=models.CASCADE)
    archivo=models.ImageField(null=True,blank=True,max_length=255)
    cita_extracciones=models.ForeignKey(CitaExtracciones,on_delete=models.CASCADE)

class ArchivoObstetra(models.Model):
    usuaria=models.ForeignKey(User,on_delete=models.CASCADE)
    archivo=models.ImageField(null=True,blank=True,max_length=255)
    cita_obstetra=models.ForeignKey(CitaObstetra,on_delete=models.CASCADE)

class ArchivoCurvaLarga(models.Model):
    usuaria=models.ForeignKey(User,on_delete=models.CASCADE)
    archivo=models.ImageField(null=True,blank=True,max_length=255)
    cita_curva_larga=models.ForeignKey(CurvaLarga,on_delete=models.CASCADE)
    