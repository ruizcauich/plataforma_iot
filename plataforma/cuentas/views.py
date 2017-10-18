from django.shortcuts import render
from .forms import FormularioUsuario
def registrar(request):
    form = FormularioUsuario()
    context={
        'form':form
    } 
    return render(request, 'cuentas/registrar.html', context)