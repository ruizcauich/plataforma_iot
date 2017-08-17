from django.shortcuts import render


def index(request):
    context = { }

    return render(request,'inicio.html',context)

def about(request):

    context = { }

    return render(request, 'acerca_de.html',context)