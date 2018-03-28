#IMPORTS DJANGO
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.contrib.auth.models import User
#IMPORTS PLATAFORMA
from .models import Proyecto, Dispositivo, Sensor
from .forms import FormProyecto,FormDispositivo
import json


@login_required(login_url = 'cuentas:login')
def index(request):
    usuario = User.objects.get(username=request.user)
    proyectos = Proyecto.objects.filter(usuario=request.user)
    numero_proyectos = proyectos.count()
    numero_dispositivos = 0
    numero_sensores = 0
    for pro in proyectos:
        for dis in pro.dispositivo_set.all():
            numero_dispositivos+=1
            for sen in dis.sensor_set.all():
                numero_sensores+=1

    context = {
        'proyectos': proyectos,
        'numero_proyectos':numero_proyectos,
        'numero_dispositivos':numero_dispositivos,
        'numero_sensores':numero_sensores,
        'usuario': usuario,
    }

    return render(request,'dashboard/index_n.html',context)


# ==================
#   VISTAS CORRESPONDIENTES A PROYECTOS
# ==================
# VISTA PARA CREAR UN PROYECTO
@login_required(login_url = 'cuentas:login')
def formularioProyecto(request):

    form = FormProyecto(request.POST or None)
    if form.is_valid():
        proyecto = form.save()
        proyecto.usuario = request.user
        form = FormProyecto()
        proyecto.save()

    
    proyectos = Proyecto.objects.filter(usuario=request.user)
    context = {
        'form': form,
        'proyectos': proyectos
    }

    return render(request,'dashboard/proyectos.html',context)


@login_required(login_url = 'cuentas:login')
def modificarProyecto(request, id):

    proyecto = get_object_or_404(Proyecto, pk=id)
    form = FormProyecto(request.POST or None, instance=proyecto)
    

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect( 'dashboard:detalle-proyecto',proyecto.id)

# VISTA ENCARGADA DE ELIMINAR UN PROYECTO
@login_required(login_url = 'cuentas:login')
def eliminarProyecto(request, id):
    proyecto = get_object_or_404(Proyecto, pk=id)
    try:
        proyecto.delete()
        return HttpResponse("Proyecto " + str(id) + " eliminado exitosamente")
    except:
        pass
    return HttpResponse("Proyecto " + str(id) + " NO eliminado exitosamente")

@login_required(login_url = 'cuentas:login')
def detalleProyecto(request, id_proyecto):
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    form = FormProyecto(instance=proyecto)
    formDisp = FormDispositivo( initial={'proyecto':str(proyecto.id)}, hide=['proyecto'])
    context= {
        'form':form,
        'formDisp': formDisp,
        'proyecto': proyecto
    }
    return render(request, 'dashboard/detalle-proyecto.html', context)


# ==================
#   VISTAS CORRESPONDIENTES A DISPOSITIVOS
# ==================
# VISTA PARA CREAR UN DISPOSITIVO
@login_required(login_url = 'cuentas:login')
def formularioDispositivo(request):

    form = FormDispositivo(request.POST or None)

    if form.is_valid():
        proyecto = form.save()
        form = FormDispositivo()

    #Obtenemos todos los proyectos, enseguida los dispositios pertenecientes a estos
    dispositivos = []
    proyectos = Proyecto.objects.filter(usuario=request.user)
    for pro in proyectos:
        dispositivos += pro.dispositivo_set.all()
    
    context = {
        'form': form,
        'dispositivos':dispositivos,
    }

    return render(request,'dashboard/dispositivos.html',context)


# VISTA PARA LA MODIFICACIÓN DE DATOS DE ALGÚN DISPOSITIVO
@login_required(login_url = 'cuentas:login')
def modificarDispositivo(request, id):
    # Se obtiene el dispositivo
    dispositivo = get_object_or_404(Dispositivo, pk=id)
    # Se llena el formulario con los datos obtenidos y se relaciona 
    # a la instancia del dispositivo correspondiente
    form = FormDispositivo(request.POST or None, instance=dispositivo)
    
    # Si el formulario es válido
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect( 'dashboard:detalle-dispositivo',dispositivo.id)

@login_required(login_url = 'cuentas:login')
def eliminarDispositivo(request, id):
    dispositivo = get_object_or_404(Dispositivo, pk=id)
    try:
        dispositivo.delete()
        return HttpResponse("Dispositivo " + str(id) + " eliminado exitosamente ")
    except:
        pass
    return HttpResponse("Dispositivo " + str(id) + " no eliminado " )


@login_required(login_url = 'cuentas:login')
def detalleDispositivo(request, id_dispositivo):
    return HttpResponse(id_dispositivo)

def obtenerCoordenadas(request, id_proyecto):
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)

    dispositivos = proyecto.dispositivo_set.all()
    lista_de_datos = []
    for dispositivo in dispositivos:
        lista_de_datos.append([dispositivo.nombre_de_dispositivo,dispositivo.latitud, dispositivo.longitud ])

    datos={
        "dispositivos" : lista_de_datos
    }

    #return HttpResponse(json.dumps(lista_dispositivos), content_type='application/json')
    #return JsonResponse( datos )
    return HttpResponse(json.dumps(datos),content_type='application/json')
    


@login_required(login_url = 'cuentas:login')
def configuracion(request):

    usuario = request.user

    context = {'usuario': usuario}

    return render(request, 'dashboard/configuracion.html', context)


@login_required(login_url = 'cuentas:login')
def redProyecto(request):

    id_proyecto = request.GET['id']

    proyecto = Proyecto.objects.get(pk = id_proyecto)
    dispositivos = Dispositivo.objects.filter(proyecto=proyecto)

    lista_dispositivos = []
    
    for dispo in dispositivos:
        dict_aux = {'dispositivos': dispo.nombre_de_dispositivo,'sensores': 0 }
        lista_sensores = []

        for sensor in Sensor.objects.filter(dispositivo = dispo.pk):
            lista_sensores.append(sensor.nombre_de_sensor)
            
        dict_aux['sensores'] = lista_sensores
        lista_dispositivos.append(dict_aux)


    return HttpResponse(json.dumps(lista_dispositivos), content_type='application/json')