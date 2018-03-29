
function ajax(proyecto_id,proyecto_nombre){
    
    ejecutarAjax("/dashboard/red-proyecto/"+proyecto_id,proyecto_id,"POST",
    function(data){
        graficar_proyecto(data.response, proyecto_nombre);
    });
    
}

function graficar_proyecto(response,proyecto_nombre){

    var nodesArray = new Array();
    var contador = 0

    var data = JSON.parse(response);


    for(var i = 0 ; i < data.length ; i++){
        nodesArray.push({id: i+1, label: data[i].dispositivos ,group:2});
        contador++;
    }

    
    var nodes = new vis.DataSet(nodesArray);

    
    
    for(var i = 0; i < nodesArray.length; i++){
        for( var j = 0; j < data[i].sensores.length; j++){
            nodes.add({id: contador+1, label: data[i].sensores[j], group:3, nombreDispositivo: data[i].dispositivos})
            contador++;
        }
    }

    nodes.add({id: 0, label: proyecto_nombre, group:1, first:true, fixed: false})
    

    var nodesEdges = new Array();
    

    var proyecto =  nodes.get(0);
    var dispositivos = nodes.get({filter: function(item){return item.group == 2;}})
    var sensores = nodes.get({filter: function(item){return item.group == 3;}})
    


    for(var i = 0; i < dispositivos.length; i++){
        nodesEdges.push( {from: proyecto.id, to: dispositivos[i].id});
        for(var j = 0; j < sensores.length; j++){
            if( dispositivos[i].label == sensores[j].nombreDispositivo){
                nodesEdges.push({from: dispositivos[i].id, to: sensores[j].id});
            }
        }
    }


    var edges = new vis.DataSet(nodesEdges);

    //Create a network
    var container = document.getElementById('red')

    //provide the data in the vis format
    var data = {nodes: nodes, edges: edges};

    var options = {
        nodes:{
            shape: 'dot',
            size: 20,
            font:{
                size: 12,
                color: '#38477a',
            },
            borderWidth: 2
        },
        edges: {
            width: 3
        },
    }


    //Initialize your network!
    var network =  new vis.Network(container,data,options)

}