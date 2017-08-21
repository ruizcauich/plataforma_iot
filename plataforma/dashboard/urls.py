from django.conf.urls import url, include
from . import views

app_name = 'dashboard'

urlpatterns = [
    #dashboard/
    url(r'^$', views.index ,name='index'),
    #dashboard/proyecto
    url(r'^proyectos/$', views.formularioProyecto, name = 'proyectos')    
]
