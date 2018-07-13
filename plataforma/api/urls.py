from django.conf.urls import url, include
from . import views

app_name = 'api'

urlpatterns = [
    url(r'guardar_json/$',views.guardar_json, name = 'guardar-json'),
    url(r'guardar_datos/$',views.guardar_datos, name= 'guardar-datos'),
    url(r'^lecturas/([0-9]+)$', views.obtenerDatos ,name='obtener-lecturas'),
    url(r'^lecturas/([0-9]+)/ultimas$', views.obtenerUltimasLecturas ,name='obtener-ultimas-lecturas'),
]
