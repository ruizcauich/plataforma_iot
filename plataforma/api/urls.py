from django.conf.urls import url, include
from . import views

app_name = 'api'

urlpatterns = [
    url(r'guardar_json/$',views.guardar_json, name = 'guardar-json'),
    url(r'guardar_datos/$',views.guardar_datos, name= 'guardar-datos')
]
