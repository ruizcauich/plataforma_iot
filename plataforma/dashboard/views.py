from django.shortcuts import render, get_object_or_404, redirect
from .models import Proyecto, Dispositivo
from .forms import formProyecto,formDispositivo
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url = 'cuentas:login')
def index(request):
    numero_proyectos = Proyecto.objects.count()
    numero_dispositivos = Dispositivo.objects.count()
    context = { 
        'numero_proyectos':numero_proyectos,
        'numero_dispositivos':numero_dispositivos,
    }

    return render(request,'dashboard/plataforma-ejemplo.html',context)


def formularioProyecto(request):

    form = formProyecto(request.POST or None)
    if form.is_valid():
        proyecto = form.save()
        form = formProyecto()

    
    proyectos = Proyecto.objects.all()
    context = {
        'form': form,
        'proyectos': proyectos
    }

    return render(request,'dashboard/proyectos.html',context)
def modificarProyecto(request, id):

    proyecto = get_object_or_404(Proyecto, pk=id)
    form = formProyecto(request.POST or None, instance=proyecto)
    

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect( 'dashboard:detalle-proyecto',proyecto.id)


def formularioDispositivo(request):

    form = formDispositivo(request.POST or None)

    if form.is_valid():
        proyecto = form.save()
        form = formDispositivo()

    
    dispositivos = Dispositivo.objects.all()
    context = {
        'form': form,
        'dispositivos':dispositivos,
    }

    return render(request,'dashboard/dispositivos.html',context)

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
    

def detalleDispositivo(request, id_dispositivo):
    return HttpResponse(id_dispositivo)