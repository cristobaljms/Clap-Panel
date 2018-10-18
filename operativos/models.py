from django.db import models
from beneficiarios.models import Beneficiarios
# Create your models here.

class Operativo(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)
    nbolsas = models.IntegerField(default=0)
    nbolsasForaneas = models.IntegerField(default=0)
    responsable = models.CharField(max_length=255, default='')
    proveedor = models.CharField(max_length=255, default='')
    beneficiario = models.ManyToManyField(Beneficiarios)