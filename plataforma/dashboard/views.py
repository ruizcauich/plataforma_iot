from django.shortcuts import render

# Create your views here.

def index(request):

    context = { }

    return render(request,'dashboard/plataforma-ejemplo.html',context)
