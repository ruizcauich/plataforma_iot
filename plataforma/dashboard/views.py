from django.shortcuts import render
from .models import Proyecto, Dispositivo
from .forms import formProyecto,formDispositivo

# Create your views here.

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
