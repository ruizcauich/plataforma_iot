#IMPORTS DE DJANGO
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
#IMPORTS PLATAFORMA
from dashboard.models import Proyecto, Dispositivo, Sensor, Campo, Valor
#IMPORTS PYTHON
import json, math
from datetime import datetime

# Función para procesar el JSON enviado por los dispositivos
@csrf_exempt
def guardar_json(request):

    '''
    {
        "proyecto": "13A2004090C47D",
        "dispositivo": "13A20040B7D71A",
        "fecha": "22/6/2018",
        "hora": "16:48:8",
        "id_paquete": 1,
        "sensores":[{
            "nombre":"sensor1", 
            "datos":{
                    "temperatura":27,
                    "humedad":38
                }
            }
        ]
    }
    '''
    #Se tiene que determinar si se recibe algún json
    try:
        json_recibido = json.loads(request.body.decode('utf-8'))
    except:
        return HttpResponse("Su estructura json no esta bien formada")
    
    # Se tiene que determinar si la red existe
    try:
        proyecto = Proyecto.objects.get(pk = json_recibido["proyecto"])
    except:
        return HttpResponse('Proyecto no encontrado')
    # Se determina si existe el dispositivo
    try:
        dispositivo = Dispositivo.objects.get(pk = json_recibido["dispositivo"])
    except:
        return HttpResponse('dispositivo no encontrado')
    # Se emplean para generar un mensaje de respuesta
    registrado = 'Registrados: '
    no_encontrados = 'Sensores no encontrados: '
    # Intenta obtener una fecha y hora del JSON
    try:
        # Obtiene la fecha (date=dt) y separa dia, mes año
        dt = json_recibido["fecha"].split("/")
        # Convierte los datos de la fecha a números enteros
        dt = [int(val) for val in dt]
        # Obtiene la hora y separa sus componentes
        hr = json_recibido["hora"].split(":")
        # Convierte hora, minuto y segundo a números enteros
        hr = [int(val) for val in hr]
        # Crea un objeto datetime a partir de los datos anteriores
        date_time = datetime(day = dt[0], month=dt[1], year=dt[2], hour=hr[0], minute=hr[1], second=hr[2])
    except:
        # Si no hay fecha y hora en el JSON, se genera una por defecto.
        date_time = datetime(day = 1, month=1, year=2018, hour=0, minute=0, second=0)
    id_paquete = json_recibido["id_paquete"]
    print(json_recibido)
    #En caso de que sensores no existan u ocurra una excepcion al insertar en la base de datos
    try:
        # Obtiene la lista de sensores
        sensores = json_recibido["sensores"]
        # Recorre la lista
        for sensor in sensores:
            print(sensor)
            # Intenta obtener de la base de datos el sensor correspondiente
            try:
                objeto_sensor = dispositivo.sensor_set.get(nombre_de_sensor = sensor["nombre"])
            except:
                # Si no está registrado, se agrega a los "no_encontrados"
                no_encontrados += sensor["nombre"] +", "
                # Pasa al siguiente sensor en la lista
                continue
            # Obtienen los datos (lecturas) del sensor
            datos = sensor["datos"]
            # Agrega el sensor a los resgistrados
            registrado += "SENSOR-> " + sensor["nombre"] +"["
            # Por cada par clave-valor que representan el nombre del campo
            # y el valor de la lectura asociada
            for k,v in datos.items():
                #Se trae el campo a insertar
                campo = objeto_sensor.campo_set.get( nombre_de_campo = k)
                # Creamos un nuevo Valor_De_Campo perteneciente al conjunto de este
                valor = campo.valor_set.create(valor = str(v))
                # Establece la hora y fecha
                valor.fecha_dispositivo=date_time
                valor.id_paquete = id_paquete
                # Guarda los cambios en la base de datos
                valor.save()
                registrado += "Campo: " + k + ",  "

            registrado += "]"
    # Retorna respuesta, segun haya ocurrido un error o no
    except:
        return HttpResponse("Pudo harber ocurrido un error. Registro de transacion: " + no_encontrados + registrado)
    
    return HttpResponse("Registro de transaccion: "+ no_encontrados + registrado)


def validar_datos(proyecto,dispositivo,sensor):

    aceptado = False

    try:
        validar_proyecto = Proyecto.objects.get(pk = proyecto)
        validar_dispositivo = Dispositivo.objects.get(pk = dispositivo)
        validar_sensor = Sensor.objects.get(pk = sensor)
        
        aceptado = True

    except ObjectDoesNotExist:
        aceptado = False
        
    
    return aceptado
    

'''
GET /api/guardar_datos/?proyecto=1&dispositivo=1&sensor=1&campo=2.5 HTTP/1.1
'''
@csrf_exempt
def guardar_datos(request):

    if request.method == 'POST':
        diccionario_peticion = request.POST.copy()
    else:
        diccionario_peticion = request.GET.copy()

    proyecto =  diccionario_peticion['proyecto']
    del diccionario_peticion['proyecto']

    dispositivo = diccionario_peticion['dispositivo']
    del diccionario_peticion['dispositivo']

    sensor = diccionario_peticion['sensor']
    del diccionario_peticion['sensor']

    '''
    Inserción de todos los nuevos valores
    '''
    cadena = ''
    if validar_datos(proyecto,dispositivo,sensor):
        
        #Dividimos por parejas campo y valor
        for k,v in diccionario_peticion.items():
            cadena+= ' ' + k + ' ' + v  + ' // '
            
            campo = Campo.objects.get( nombre_de_campo = k )
            valor = Valor(campo = campo, valor = v)
            valor.save()

    else:
        return HttpResponse('Error en los datos')
    
    return HttpResponse('datos insertados ' + cadena)

# Función que obtiene de la base de datos un máximo de 100
# por campo en cada dispositivo
def obtenerDatos(request, dispositivo):
    lista_datos =[]
    # Ejecuta una consulta SQL cruda por medio de la función raw del ORM 
    # Para obtener el número de campos relacionados a un dispositivo
    num_campos = Campo.objects.raw('''SELECT COUNT(nombre_de_campo) AS numCampos, dashboard_campo.id FROM  dashboard_campo, dashboard_sensor
    WHERE  dashboard_campo.sensor_id=dashboard_sensor.id AND
    dashboard_sensor.dispositivo_id='''+str(dispositivo))[0].numCampos
    # Consulta que obtiene las lecturas almacenadas hasta el momento, con un límite
    # del número de campos multiplicado por 100
    lista_raw = Valor.objects.raw(
    '''
    SELECT t2.id, valor, fecha_hora_lectura, campo_id,  nombre_val  
    FROM 
    (SELECT dashboard_campo.id,  CONCAT(CONCAT(dashboard_sensor.nombre_de_sensor,'_'),dashboard_campo.nombre_de_campo) AS 'nombre_val' 
        FROM dashboard_campo INNER JOIN dashboard_sensor 
        ON (dashboard_campo.sensor_id=dashboard_sensor.id AND dashboard_sensor.dispositivo_id='''+ str(dispositivo) +''')) AS t1 
    INNER JOIN (SELECT * FROM dashboard_valor ORDER BY id  DESC LIMIT 4000) AS t2 
    ON (t1.id=t2.campo_id) ORDER BY fecha_hora_lectura DESC LIMIT '''+ str( num_campos*100 ) +''';
    '''
    )
    # Crea una lista con los datos necesarios para graficar: fecha y nombre del valor.
    lista_datos = [ {"fecha": ele.fecha_hora_lectura, ele.nombre_val:ele.valor} for ele in lista_raw if not math.isnan(float(ele.valor))]
    # ORdena los datos por la fecha
    lista_datos.sort(key=lambda registro:registro["fecha"])
    # Para cada lectura convierte el formato de la fecha
    for ele in lista_datos:
        ele["fecha"] = ele["fecha"].ctime()
    # Regresa las lecturas en formato JSON
    return HttpResponse( json.dumps(lista_datos), content_type="application/json" )
    
# Función que obtiene las ultimas lecturas almacenadas en un intervalo de 1 segundo
def obtenerUltimasLecturas(request, dispositivo):
    #dispositivo = get_object_or_404(Dispositivo, pk=dispositivo)
    lista_datos =[]
    # Para obtener el número de campos relacionados a un dispositivo
    num_campos = Campo.objects.raw('''SELECT COUNT(nombre_de_campo) AS numCampos, dashboard_campo.id FROM  dashboard_campo, dashboard_sensor
    WHERE  dashboard_campo.sensor_id=dashboard_sensor.id AND
    dashboard_sensor.dispositivo_id='''+str(dispositivo))[0].numCampos
    # Consulta que obtiene las ultimas lecturas almacenadas hasta el momento
    # en un intervalo de 1 segundo
    lista_raw = Valor.objects.raw(
    '''
    SELECT t2.id, valor, fecha_hora_lectura, campo_id,  nombre_val  
    FROM 
    (SELECT dashboard_campo.id,  CONCAT(CONCAT(dashboard_sensor.nombre_de_sensor,'_'),dashboard_campo.nombre_de_campo) AS 'nombre_val' 
        FROM dashboard_campo INNER JOIN dashboard_sensor 
        ON (dashboard_campo.sensor_id=dashboard_sensor.id AND dashboard_sensor.dispositivo_id='''+ str(dispositivo) +''')) AS t1 
    INNER JOIN (SELECT * FROM dashboard_valor ORDER BY id  DESC LIMIT 4000) AS t2 
    ON (t1.id=t2.campo_id) WHERE fecha_hora_lectura > DATE_SUB( CURRENT_TIMESTAMP(), INTERVAL 1 SECOND) 
    ORDER BY fecha_hora_lectura DESC LIMIT '''+ str( num_campos ) +''';
    '''
    )
    # Genera la lista de lecturas
    for el in lista_raw:
        if not math.isnan( float(el.valor) ) :
            dato = {
                # Convierte el formato de la fecha 
                "fecha": el.fecha_hora_lectura.ctime(),
                el.nombre_val :el.valor
            }
            lista_datos.append(dato)
    # Retorna las lecturas en formato JSON
    return HttpResponse( json.dumps(lista_datos), content_type="application/json" )

