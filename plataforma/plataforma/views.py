from django.shorcuts import render


def inicio(request):
    contexto = { }

    return render(request,'inicio.html',contexto)

def acerca_de(request):

    contexto = { }

    return render(request, 'acerca_de.html',contexto)