from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EstadoPago(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    pago_completado = models.BooleanField(default=False)