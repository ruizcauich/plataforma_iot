from django.contrib import admin
from .models import Proyecto, Dispositivo,Sensor,Campo,Valor

admin.site.register(Proyecto)
admin.site.register(Dispositivo)
admin.site.register(Sensor)
admin.site.register(Campo)
admin.site.register(Valor)

