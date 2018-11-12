from django.db import models
from beneficiarios.models import Beneficiarios
# Create your models here.

class Operativo(models.Model):
    fecha = models.DateField(auto_now_add=True)
    status = models.IntegerField(default=1)
    nbolsas = models.IntegerField(default=0)
    nbolsasForaneas = models.IntegerField(default=0)
    responsable = models.CharField(max_length=255, default='')
    proveedor = models.CharField(max_length=255, default='')

class Entrega(models.Model):
    beneficiario = models.ForeignKey(Beneficiarios, on_delete=models.CASCADE)
    operativo = models.ForeignKey(Operativo, on_delete=models.CASCADE)
    comision_servicio = models.IntegerField(default=0)
    nbolsas = models.IntegerField(default=1)
    especial = models.IntegerField(default=0)
    observacion = models.CharField(max_length=255, default='')
