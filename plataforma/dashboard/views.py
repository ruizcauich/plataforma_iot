from django.shortcuts import render, get_object_or_404, redirect
from .models import Proyecto, Dispositivo
from .forms import formProyecto,formDispositivo
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

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