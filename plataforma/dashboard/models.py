from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Proyecto(models.Model):
    usuario = models.ForeignKey(User, default=1)
    nombre_de_proyecto = models.CharField( max_length = 80)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre_de_proyecto


class Dispositivo(models.Model):
    nombre_de_dispositivo = models.CharField(max_length = 80)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=40)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    esta_habilitado = models.BooleanField(default = True)
    fecha_creacion = models.DateTimeField( auto_now_add=True )
    # apikey no está implemetado por el momento
    # apikey
    proyecto = models.ForeignKey(Proyecto, default = 1)

    def __str__(self):
        return self.nombre_de_dispositivo


class Sensor(models.Model):
    nombre_de_sensor = models.CharField(max_length=40)
    tipo = models.CharField(max_length = 40)
    fecha_creacion = models.DateTimeField( auto_now_add=True )
    esta_habilitado = models.BooleanField(default = True)
    dispositivo = models.ForeignKey(Dispositivo, default = 1)
    
    def __str__(self):
        return self.nombre_de_sensor


class Campo( models.Model):
    nombre_de_campo = models.CharField(max_length=30)
    tipo_de_valor = models.CharField(max_length=40)
    sensor = models.ForeignKey(Sensor, default = 1)

    def __str__(self):
        return self.nombre_de_campo


class Valor(models.Model):
    valor = models.CharField(max_length=100)
    fecha_hora_lectura = models.DateTimeField(auto_now_add=True)
    fecha_dispositivo = models.DateTimeField(blank=True, null=True)
    campo = models.ForeignKey(Campo, default = 1)

    def __str__(self):
        return self.valor