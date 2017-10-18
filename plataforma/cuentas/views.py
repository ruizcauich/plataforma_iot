from django.shortcuts import render, redirect
from .forms import FormularioUsuario
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def registrar(request):
    
    form = FormularioUsuario(request.POST or None)

    if form.is_valid():
        usuario = form.save(commit=False)
        usuario.set_password(form.cleaned_data['password'])
        usuario.save()
        usuario = authenticate(username=usuario.username, password=form.cleaned_data['password'])
        login(request,usuario)
        return redirect('dashboard:index')


    context={
        'form':form
    } 
    return render(request, 'cuentas/registrar.html', context)