#importación del paquete forms
from django import forms
#importación de la clase User
from django.contrib.auth.models import User

#Declaración de clase FormularioUsuario.  Hereda de ModelForm
class FormularioUsuario(forms.ModelForm):
    #Campo contraseña para la cuenta de usuario
    password = forms.CharField(widget=forms.PasswordInput)

    #Clase Meta donde se especifican información que usa la clase 
    class Meta:
        #Indica el modelo relacionado al formulario
        model = User
        #Campos requeridos para el formulario
        fields = ['username', 'email', 'password']

