from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from dashboard.models import Proyecto, Dispositivo, Sensor, Campo
from django.core.urlresolvers import reverse
import json

# Create your views here.

def guardar_json(request):
    
    return HttpResponse('Guardar_Json')