from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class CitaMedicinaFamilia(models.Model):
    usuaria=models.ForeignKey(User,on_delete=models.CASCADE)
    fecha=models.DateTimeField(null=True,blank=True)
    receta_acido_folico=models.BooleanField(null=True,blank=True,default=False)
    receta_hierro=models.BooleanField(null=True,blank=True,default=False)
    observaciones=models.CharField(null=True,blank=True,max_length=255)
    trimestre=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])
    tipo=models.CharField(null=True,blank=True)