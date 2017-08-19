from django.db import models

# Create your models here.
class Proyecto(models.Model):
    nombre_de_proyecto = models.CharField( max_length = 80)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre_de_proyecto


class Dispositivo(models.Model):
    nombre_de_dispositivo = models.CharField(max_length = 80)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=40)
    latitud = models.FloatField()
    longitud = models.FloatField()
    esta_habilitado = models.BooleanField(default = True)
    fecha_creacion = models.DateTimeField( auto_now_add=True )
    # apikey no está implemetado por el momento
    # apikey

    def __str__(self):
        return self.nombre_de_dispositivo


class Sensor(models.Model):
    nombre_de_sensor = models.CharField(max_length=40)
    tipo = models.CharField(max_length = 40)
    fecha_creacion = models.DateTimeField( auto_now_add=True )
    esta_habilitado = models.BooleanField(default = True)

class Campo( models.Model):
    nombre_de_campo = models.CharField(max_length=30)
    tipo_de_valor = models.CharField(max_length=40)

class Valor(models.Model):
    valor = models.CharField(max_length=100)
    fecha_hora_lectura = models.DateTimeField(auto_now_add=True)