var ejesDeGrafica = [];
var  confi_de_graficos = [];
var chart;

function generarInfoParaGrafica(ejes){
    // naranja, azul, rojo, verde, morado, 
    var colors = ["#ff681f","#02a4d3","#d92121", "#3aa655", "#639"];
    var offset = 0;
    var aumentoOffset = 50;
    for(var item=0;item < ejes.length; item++){
    confi_de_graficos.push({
        "valueAxis": "v"+item,
        "lineColor": colors[item],
        "bullet": "round",
        "bulletBorderThickness": 10,
        //"hideBulletsCount": 30,
        "title": ejes[item],
        "valueField": ejes[item],
        "fillAlphas": 0.0,
        "balloonText": "[[category]]: <b>[[value]]</b>",
    });

    ejesDeGrafica.push({
            "id":"v"+item,
            "axisColor": colors[item],
            "axisThickness": 2,
            "axisAlpha": 1,
            "position": "left",
            "offset": offset+=aumentoOffset,
    });
}


}

function graficar( data ){
    var ejes = [];
    for(d of data){
        d.fecha = new Date(d.fecha);
        for( atributo in d ){
            if(!ejes.includes(atributo) && atributo!='fecha'){
                ejes.push(atributo);
            }
        }
    }
    generarInfoParaGrafica(ejes);
    chart = AmCharts.makeChart( "chart", {
        "type": "serial",
        "theme": "light",
        "legend": {
            "useGraphSettings": true
        },
        "marginRight":80,
        "dataProvider":data,
        "synchronizeGrid":true,
        "dataDateFormat": "YYYY-MM-DD HH:NN:SS",
        "gridAboveGraphs": true,
        //"startDuration": 1,
        "valueAxes": //ejesDeGrafica,
        [ {
            "gridColor": "#FFFFFF",
            "gridAlpha": 0.2,
            "dashLength": 0
        } ],
        "graphs":confi_de_graficos,
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

var dat;
var aj = new XMLHttpRequest();
aj.onreadystatechange = function(){
    if(this.readyState == 4 && this.status==200){
        console.log(this.responseText);
        dat = JSON.parse(this.responseText);
        console.log(dat);
        if(dat.length==0){
            var avisoModal = new LIBRERIA.Modal("Aviso");
            avisoModal.informacion();
            avisoModal.reducido();
            avisoModal.encabezado.innerHTML="<h1>Oops!</h1>"
            avisoModal.cuerpo.innerHTML ="<p>Al parecer aun no hay registros de tus sensores.</p>"
            avisoModal.abrir();
            setTimeout(function(){ avisoModal.cerrar()}, 3500);
        }
        graficar( dat );
    }
}

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

setInterval( function() {
    var realTimeRequest = new XMLHttpRequest();
    // normally you would load new datapoints here,
    // but we will just generate some random values
    // and remove the value from the beginning so that
    // we get nice sliding graph feeling
  
    // remove datapoint from the beginning
    //chart.dataProvider.shift();
  
    // add new one at the end
    realTimeRequest.onreadystatechange = function(){
        if(this.readyState == 4 && this.status==200 && chart!=null){
            console.log(this.responseText);
            var rtDat
            rtDat = JSON.parse(this.responseText);
            
            for( valores of rtDat ){
                valores.fecha = new Date(valores.fecha)
                console.log(valores.fecha)
               chart.dataProvider.push( valores);
               chart.dataProvider.shift();
            }
            chart.validateData();
            
            
        }
    }

    realTimeRequest.open("GET", urlRT, true);
    realTimeRequest.send();
    


    
  }, 1000 );