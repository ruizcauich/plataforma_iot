from django.shortcuts import render
from .models import Proyecto, Dispositivo
from .forms import formProyecto,formDispositivo

# Create your views here.

def index(request):

    context = { }

    return render(request,'dashboard/plataforma-ejemplo.html',context)


def formularioProyecto(request):

    form = formProyecto(request.POST or None)

    if form.is_valid():
        proyecto = form.save()
        form = formProyecto()

    
    
    context = {'form': form}

    return render(request,'dashboard/formProyecto.html',context)


def formularioDispositivo(request):

    form = formDispositivo(request.POST or None)

    if form.is_valid():
        proyecto = form.save()
        form = formDispositivo()

    
    
    context = {'form': form}

    return render(request,'dashboard/formDispositivo.html',context)
