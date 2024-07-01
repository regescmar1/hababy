from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CitaOdontologia(models.Model):
    usuaria=models.ForeignKey(User,on_delete=models.CASCADE)
    fecha=models.DateTimeField(null=True,blank=True)
    limpieza =models.BooleanField(null=True,blank=True,default=False)
    observaciones=models.CharField(null=True,blank=True,max_length=255)