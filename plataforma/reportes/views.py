#IMPORTS DJANGO
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.contrib.auth.models import User
#IMPORTS PLATAFORMA
from dashboard.models import Proyecto, Dispositivo, Sensor, Campo, Valor
import json, math

@login_required(login_url = 'cuentas:login')
def index(request):
    return render(request,'reportes/index.html',{'usuario':request.user})

@login_required(login_url = 'cuentas:login')
def graficar(request, dispositivo):
    return render(request, "reportes/grafica.html", {'dispositivo':dispositivo})


def obtenerDatos(request, dispositivo):
    dispositivo = get_object_or_404(Dispositivo, pk=dispositivo)
    lista_datos =[]
    numCampos = 0
    for sensor in dispositivo.sensor_set.all(): 
        for campo in sensor.campo_set.all():
            numCampos+=1
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
    
    return HttpResponse(json.dumps(lista_datos[:numCampos*50]), content_type="application/json")
    

def obtenerUltimasLecturas(request, dispositivo):
    #dispositivo = get_object_or_404(Dispositivo, pk=dispositivo)
    lista_datos =[]
    num_campos = Campo.objects.raw('''SELECT COUNT(nombre_de_campo) AS numCampos, dashboard_campo.id FROM  dashboard_campo, dashboard_sensor
    WHERE  dashboard_campo.sensor_id=dashboard_sensor.id AND
    dashboard_sensor.dispositivo_id='''+str(dispositivo))[0].numCampos
    lista_raw = Valor.objects.raw(
    '''
    SELECT  dashboard_valor.id, valor, fecha_hora_lectura, campo_id,  CONCAT(CONCAT(dashboard_sensor.nombre_de_sensor,'_'),dashboard_campo.nombre_de_campo)AS 'nombre_val'
    from dashboard_valor, dashboard_campo, dashboard_sensor
    WHERE dashboard_valor.campo_id = dashboard_campo.id AND dashboard_campo.sensor_id=dashboard_sensor.id AND dashboard_sensor.dispositivo_id='''+str(dispositivo)+''' GROUP BY fecha_hora_lectura 
    ORDER BY fecha_hora_lectura ASC LIMIT '''+str(num_campos)+''' ;
    '''
    )
    
    for el in lista_raw:
        if not math.isnan( float(el.valor) ) :
            dato = {
                "fecha": el.fecha_hora_lectura.ctime(),
                el.nombre_val :el.valor
            }
            lista_datos.append(dato)
    
    return HttpResponse( json.dumps(lista_datos) )

