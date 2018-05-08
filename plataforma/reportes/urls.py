from django.conf.urls import url, include
from . import views

app_name = 'reportes'

urlpatterns = [
    #dashboard/
    url(r'^$', views.index ,name='index'),
    url(r'^graficar/([0-9]+)$', views.graficar ,name='graficar'),
    url(r'^obtener-datos/([0-9]+)$', views.obtenerDatos ,name='obtener-datos'),
    url(r'^obtener-realtime/([0-9]+)$', views.obtenerUltimasLecturas ,name='obtener-realtime'),
    url(r'^estadisticas/$', views.index ,name='estadisticas'),
    
]
