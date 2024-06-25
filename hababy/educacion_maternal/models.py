from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Sesion(models.Model):
    usuaria=models.ForeignKey(User,on_delete=models.CASCADE)
    fecha=models.DateTimeField(null=True,blank=True)
    titulo=models.CharField()
    observaciones=models.CharField(null=True,blank=True,max_length=255)