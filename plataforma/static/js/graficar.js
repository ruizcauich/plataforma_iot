// Ejes Y de la gráfica
var ejesY = [
    {   "id":"temp",
        "axisColor": "#996633",
        "axisThickness": 2,
        "axisAlpha": 1,
        "position": "left",
        "offset": 0,
        "title":"° C"
    }, {
        "id":"hum",
        "axisColor": "#999966",
        "axisThickness": 2,
        "axisAlpha": 1,
        "position": "right",
        "offset": 40,
        "title":"Humedad"
    }, {
        "id":"default",
        "axisColor": "#000000",
        "axisThickness": 2,
        "axisAlpha": 1,
        "position": "left",
        "offset": 0,
    }];
var  confi_de_graficos = [];
var chart // El objeto chart de AmCharts;

function generarInfoParaGrafica(etiquetas){
    // naranja, azul, rojo, verde, morado, 
    var colors = ["#ff681f","#02a4d3","#d92121", "#3aa655", "#639"];
    var offset = 0;
    var aumentoOffset = 50;
    for(var item=0;item < etiquetas.length; item++){
        var valueAxisIdentifier = "default"; // Default id para el Axis (eje Y)
        // Determina si corresponde al eje de temperatura o humedad
        if(etiquetas[item].toLowerCase().includes("temp")){
            valueAxisIdentifier = "temp"
        }
        if( etiquetas[item].toLowerCase().includes("hum") ){
            valueAxisIdentifier = "hum"
        }
        // Catrgoriza las etiquetas y asigna el respectivo eje
        confi_de_graficos.push({
            "valueAxis": valueAxisIdentifier,
            "lineColor": colors[item],
            "bullet": "round",
            "bulletBorderThickness": 10,
            "title": etiquetas[item],
            "valueField": etiquetas[item], // campo correspondiente para tomar el valor
            "fillAlphas": 0.0,
            "balloonText": "[[category]]: <b>[[value]]</b>",
        });
    }
}
// Función que toma los datos y configura la graficación
function graficar( data ){
    var etiquetas = [];
   
    for(d of data){
         // Para convertir a objeto fecha 
        d.fecha = new Date(d.fecha);
        for( atributo in d ){
            // Genera un arreglo de etiquetas
            if(!etiquetas.includes(atributo) && atributo!='fecha'){
                etiquetas.push(atributo);
            }
        }
    }
    // Ejecuta la función que categoriza los datos para graficar
    generarInfoParaGrafica(etiquetas);
    // Crea un objeto de AmCharts y configura la gráfica
    chart = AmCharts.makeChart( "chart", {
        "type": "serial",
        "theme": "light",
        "legend": {
            "useGraphSettings": true
        },
        "marginRight":80,
        "dataProvider":data,// Todos los datos en JSon
        "synchronizeGrid":true,
        "dataDateFormat": "YYYY-MM-DD HH:NN:SS",
        "gridAboveGraphs": true,
        "valueAxes": ejesY, // Los tres ejes Y
       /* [ {
            "gridColor": "#FFFFFF",
            "gridAlpha": 0.2,
            "dashLength": 0
        } ],*/
        "graphs":confi_de_graficos, // Clasifica los datos y etiquetas
        "chartCursor": {
            "categoryBalloonEnabled": false,
            "cursorAlpha": 0,
            "zoomable": false
        },
        "categoryField": "fecha",
        "categoryAxis": {
            "minPeriod": "ss",
            "parseDates": true,
            "gridPosition": "start",
            "gridAlpha": 0,
            //"tickPosition": "start",
            //"tickLength": 20,
            "labelRotation": 45,
            "ignoreAxisHigth":true,
            //"autoWrap":true
        },
        "chartScrollbar": {},
        "export": {
            "enabled": true,
            "dateFormat": "YYYY-MM-DD HH:NN:SS"
            
        },
        

    } );
}
// Para almacenar las lecturas
var dat;
// Objeto empleado para crear la petición
var aj = new XMLHttpRequest();
aj.onreadystatechange = function(){
    // Hay una respuesta sin errores
    if(this.readyState == 4 && this.status==200){
        console.log(this.responseText);
        // Se convierte de texto a estructura de datos para JavaScript
        dat = JSON.parse(this.responseText);
        console.log(dat);
        // Si no hay lecturas, se despliega un aviso
        if(dat.length==0){
            var avisoModal = new LIBRERIA.Modal("Aviso");
            avisoModal.informacion();
            avisoModal.reducido();
            avisoModal.encabezado.innerHTML="<h1>Oops!</h1>"
            avisoModal.cuerpo.innerHTML ="<p>Al parecer aun no hay registros de tus sensores.</p>"
            avisoModal.abrir();
            setTimeout(function(){ avisoModal.cerrar()}, 3500);
        }
        // Se envian los tados para graficar
        graficar( dat );
    }
}
// Se ejecuta la petición
aj.open("GET", url, true);
aj.send();


function otravez( max){
    ejesDeGrafica = [];
    confi_de_graficos=[];
    var td = []
    max = (max>0)? max:dat.length-1;
    for(var i = dat.length-1 -max; i < dat.length-1; i++){
        td.push(dat[i]);
    }
    graficar(td);
}
function mostrarNumeroRegistros(){
    var txtNumeroRegistros = document.getElementById("txtNumeroRegistros");
    var numeroRegistros = parseInt(txtNumeroRegistros.value);
    otravez(numeroRegistros);

}
// Se crea una función que realice una petición HTTP cada segundo
setInterval( function() {
    // Objeto empleado para crear la petición
    var realTimeRequest = new XMLHttpRequest();
    // normally you would load new datapoints here,
    // but we will just generate some random values
    // and remove the value from the beginning so that
    // we get nice sliding graph feeling
  
    // remove datapoint from the beginning
    //chart.dataProvider.shift();
  
    // add new one at the end
    realTimeRequest.onreadystatechange = function(){
        // Hay una respuesta sin errores
        if(this.readyState == 4 && this.status==200 && chart!=null){
            console.log(this.responseText);
            var rtDat
            // Se convierte de texto a estructura de datos para JavaScript
            rtDat = JSON.parse(this.responseText);
            
            for( valores of rtDat ){
                // Para cada lectura se crea una fecha
                valores.fecha = new Date(valores.fecha)
                console.log(valores.fecha)
                // Se anexa la nueva lectura a la gráfica
               chart.dataProvider.push( valores);
               chart.dataProvider.shift();
            }
            // se validan los datos para graficarlos
            chart.validateData();
            
            
        }
    }
    // Se ejecuta la petición (cada segundo)
    realTimeRequest.open("GET", urlRT, true);
    realTimeRequest.send();
    
  }, 1000 );