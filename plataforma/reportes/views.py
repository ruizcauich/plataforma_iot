#IMPORTS DJANGO
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#IMPORTS PLATAFORMA
from dashboard.models import Proyecto, Dispositivo, Sensor, Campo, Valor


@login_required(login_url = 'cuentas:login')
def index(request):
    return render(request,'reportes/index.html',{'usuario':request.user})

@login_required(login_url = 'cuentas:login')
def graficar(request, dispositivo):
    return render(request, "reportes/grafica.html", {'dispositivo':dispositivo})
