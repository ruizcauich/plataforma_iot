#IMPORTS DJANGO
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.contrib.auth.models import User
#IMPORTS PLATAFORMA
from dashboard.models import Proyecto, Dispositivo, Sensor
import json

@login_required(login_url = 'cuentas:login')
def index(request):
    return render(request,'reportes/index.html',{'usuario':request.user})

@login_required(login_url = 'cuentas:login')
def graficar(request, dispositivo):
    return render(request, "reportes/grafica.html", {'dispositivo':dispositivo})

import math
def obtenerDatos(request, dispositivo):
    dispositivo = get_object_or_404(Dispositivo, pk=dispositivo)
    lista_datos =[]
    for sensor in dispositivo.sensor_set.all(): 
        for campo in sensor.campo_set.all():
            for valor in campo.valor_set.all().order_by("fecha_hora_lectura"):
                valor_valor = float(valor.valor) 
                if not math.isnan(valor_valor) :
                    dato = {
                        "fecha": valor.fecha_hora_lectura,
                        sensor.nombre_de_sensor+ "_" + campo.nombre_de_campo: valor_valor,
                    }
                    lista_datos.append(dato)
    
    lista_datos.sort(key=lambda registro:registro["fecha"])
    for ele in lista_datos:
        ele["fecha"] = ele["fecha"].ctime()
    
    return HttpResponse(json.dumps(lista_datos), content_type="application/json")
    #return HttpResponse("Bunevenido a reportes")
