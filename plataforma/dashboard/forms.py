#Importación del paquete forms
from django import forms
#Importación de modelos
from .models import Proyecto, Dispositivo, Sensor, Campo, Valor

#Declaración de la clase FormProyecto. Hereda de la Clase ModelForm 
class FormProyecto(forms.ModelForm):
    #Dentro de la clase Meta se especifica información que usa la clase
    class Meta:
        #Modelo usado
        model = Proyecto
        #Campos requeridos para el formulario
        fields = ['nombre_de_proyecto','descripcion' ]
        #Etiquetas para cada campo del modelo Proyecto
        labels = {
            'nombre_de_proyecto': 'Nombre del Proyecto',
            'descripcion': 'Descripción',
        }
    
    

class FormDispositivo(forms.ModelForm):
    class Meta:
        model = Dispositivo
        fields = '__all__'
        labels = {
            'nombre_de_dispositivo': 'Nombre del Dispositivo',
            'descripcion' : 'Descripción',
            'esta_habilitado' : 'Habilitado',
            'fecha_creacion' : 'Fecha de Creación',
        }
    def __init__(self,*args, **kwargs):
        from django.forms.widgets import HiddenInput
        hide = kwargs.pop('hide',None)
        usuario = kwargs.pop('usuario',None)
        super(FormDispositivo, self).__init__(*args, **kwargs)
        if hide:
            for field in hide:
                self.fields[field].widget = HiddenInput()

        if usuario:
            self.fields['proyecto'].queryset = Proyecto.objects.filter(usuario=usuario)

class FormSensor(forms.ModelForm):
    class Meta:
        model = Sensor
        fields = '__all__'
        labels = {
            'nombre_de_sensor': 'Nombre del Sensor',
            'esta_habilitado' : 'Habilitado',
            'fecha_creacion' : 'Fecha de Creación',
        }



class FormCampo(forms.ModelForm):
    class Meta:
        model = Campo
        fields = '__all__'
        labels = {
            'nombre_de_campo': 'Nombre del Campo',
            'tipo_de_valor' : 'Tipo de Valor',
        }



class FormValor(forms.ModelForm):
    model = Valor
    fields = '__all__'
    labels = {
        'fecha_hora_lectura' : 'Fecha y Hora',
    }

