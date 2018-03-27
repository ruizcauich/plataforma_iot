from django import forms
from .models import Proyecto, Dispositivo, Sensor, Campo, Valor

class FormProyecto(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre_de_proyecto','descripcion' ]
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
    def __init__(self, *args, **kwargs):
        from django.forms.widgets import HiddenInput
        hide = kwargs.pop('hide',None)
        super(FormDispositivo, self).__init__(*args, **kwargs)
        if hide:
            for field in hide:
                self.fields[field].widget = HiddenInput()

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

