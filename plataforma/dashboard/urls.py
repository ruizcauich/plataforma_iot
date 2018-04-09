from django.conf.urls import url, include
from . import views

app_name = 'dashboard'

urlpatterns = [
    #dashboard/
    url(r'^$', views.index ,name='index'),
    #dashboard/proyectos
    url(r'^proyectos/$', views.formularioProyecto, name = 'proyectos'), 
    #dashboard/proyectos/345
    url(r'^proyectos/([0-9]+)$', views.detalleProyecto, name = 'detalle-proyecto'),       
    url(r'^proyectos/([0-9]+)/modificar$', views.modificarProyecto, name = 'modificar-proyecto'),       
    url(r'^proyectos/([0-9]+)/eliminar$', views.eliminarProyecto, name = 'eliminar-proyecto'),       
    #dashboard/proyectos/345/obtenerCoordenadas
    url(r'^proyectos/([0-9]+)/obtenerCoordenadas$', views.obtenerCoordenadas, name = 'obtener-coordenadas'),       
    #dashboard/dispoitivos
    url(r'^dispositivos/$', views.formularioDispositivo, name = 'dispositivos'),
    #dashboard/dispositivos/nuevo
    url(r'^dispositivos/crear$', views.crearDispositivo, name = 'crear-dispositivo'),
    #dashboard/dispositivos/345
    url(r'^dispositivos/([0-9]+)$', views.detalleDispositivo, name = 'detalle-dispositivo'),
    #dashboard/dispositivos/345/modificar
    url(r'^dispositivos/([0-9]+)/modificar$', views.modificarDispositivo, name = 'modificar-dispositivo'),
    url(r'^dispositivos/([0-9]+)/eliminar$', views.eliminarDispositivo, name = 'aliminar-dispositivo'),
    #dashboard/configuracion
    url(r'^configuracion/$', views.configuracion, name='configuracion'),
    #dashboard/red-proyecto/
    url(r'^red-proyecto/([0-9]+)$', views.redProyecto, name='red-proyecto'),
]
