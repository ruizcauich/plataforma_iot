#IMPORTS DJANGO
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.contrib.auth.models import User
#IMPORTS PLATAFORMA
from .models import Proyecto, Dispositivo, Sensor
from .forms import formProyecto,formDispositivo
import json

# Create your views here.
@login_required(login_url = 'cuentas:login')
def index(request):
    proyectos = Proyecto.objects.filter(usuario=request.user)
    numero_proyectos = proyectos.count()
    numero_dispositivos = 0
    for pro in proyectos:
        for dis in pro.dispositivo_set.all():
            numero_dispositivos+=1

    context = {
        'proyectos': proyectos,
        'numero_proyectos':numero_proyectos,
        'numero_dispositivos':numero_dispositivos,
    }

    return render(request,'dashboard/plataforma-ejemplo.html',context)

@login_required(login_url = 'cuentas:login')
def formularioProyecto(request):

    form = formProyecto(request.POST or None)
    if form.is_valid():
        proyecto = form.save()
        proyecto.usuario = request.user
        form = formProyecto()
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
    form = formProyecto(request.POST or None, instance=proyecto)
    

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect( 'dashboard:detalle-proyecto',proyecto.id)


@login_required(login_url = 'cuentas:login')
def formularioDispositivo(request):

    form = formDispositivo(request.POST or None)

    if form.is_valid():
        proyecto = form.save()
        form = formDispositivo()

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


@login_required(login_url = 'cuentas:login')
def detalleProyecto(request, id_proyecto):
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)
    form = formProyecto(instance=proyecto)
    formDisp = formDispositivo( initial={'proyecto':str(proyecto.id)}, hide=['proyecto'])
    context= {
        'form':form,
        'formDisp': formDisp,
        'proyecto': proyecto
    }
    return render(request, 'dashboard/detalle-proyecto.html', context)
    


@login_required(login_url = 'cuentas:login')
def detalleDispositivo(request, id_dispositivo):
    return HttpResponse(id_dispositivo)

def obtenerCoordenadas(request, id_proyecto):
    proyecto = get_object_or_404(Proyecto, id=id_proyecto)

    dispositivos = proyecto.dispositivo_set.all()
    lista_de_datos = []
    for dispositivo in dispositivos:
        lista_de_datos.append(   [dispositivo.latitud, dispositivo.longitud ]  )

    datos={
        'dispositivos' : lista_de_datos
    }
    return JsonResponse( datos )


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