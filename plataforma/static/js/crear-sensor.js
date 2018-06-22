window.onload = inicio;

//Formulario
var nombreCampo;
var tipoValor;
var nombreSensor;
var tipoSensor;
var nombreCampoHidden;
var tipoValorCampoHidden;
//JS
var nombreCampoJs;
var tipoValorJs;
var contenedorCampos;
//
var contador = 0;
var listaTipos = [];
var listaNombres = [];  

function inicio(){
    //Formulario
    nombreCampo = document.getElementById("id_nombre_campo");
    nombreCampo.value = "";

    tipoValor = document.getElementById("id_tipo_valor");
    tipoValor.value = "";

    nombreSensor = document.getElementById("id_nombre_de_sensor");
    nombreSensor.value = "";

    tipoSensor = document.getElementById("id_tipo");
    tipoSensor.value = "";

    //JS
    nombreCampoJs = document.getElementById("id_nombre_de_campo_js");
    nombreCampoJs.value = "";

    tipoValorJs = document.getElementById("id_tipo_valor_js");
    tipoValorJs.value = "";
}

function comprobarCampos(nombreCampo,tipoValorCampo){
    if(nombreCampo == "" ||tipoValorCampo == ""){
        document.getElementById("id_nombre_de_campo_js").placeholder = "Campo Necesario";
        document.getElementById("id_nombre_de_campo_js").style.border = "1px solid #dd6d65";
        document.getElementById("id_tipo_valor_js").placeholder = "Campo Necesario";
        document.getElementById("id_tipo_valor_js").style.border = "1px solid #dd6d65";
        return false;
    }
    document.getElementById("id_tipo_valor_js").placeholder = "";
    document.getElementById("id_nombre_de_campo_js").placeholder = "";
    document.getElementById("id_nombre_de_campo_js").style.border = "";
    document.getElementById("id_tipo_valor_js").style.border = "";
    return true;
}

function dibujarCampo(nombreCampo,tipoValorCampo){
    nuevoCampo = document.createElement("div");
    nuevoCampoNombre = document.createElement("h3");
    nuevoCampoTipo = document.createElement("h5");
    eliminarCampoElemento = document.createElement("span");


    contenedorCampos = document.getElementById("campos");
    nuevoCampo.className = "campo";
    eliminarCampoElemento.className = "eliminarCampo";
    var id = "eliminar-"+ contador;
    nuevoCampo.setAttribute("id",id);

    nuevoCampoNombreContent = document.createTextNode(nombreCampo);
    nuevoCampoTipoContent = document.createTextNode(tipoValorCampo);
    eliminarCampoContent = document.createTextNode("x");

    nuevoCampoNombre.appendChild(nuevoCampoNombreContent);
    nuevoCampoTipo.appendChild(nuevoCampoTipoContent);
    eliminarCampoElemento.appendChild(eliminarCampoContent);

    nuevoCampo.appendChild(nuevoCampoNombre);
    nuevoCampo.appendChild(nuevoCampoTipo);
    nuevoCampo.appendChild(eliminarCampoElemento)
    contenedorCampos.appendChild(nuevoCampo);
}


function agregarCampo(){

    
    //Obtención de los datos del campo
    var nombreCampo = document.getElementById("id_nombre_de_campo_js").value;
    var tipoValorCampo = document.getElementById("id_tipo_valor_js").value;

    //Comprobación de campos
    if(!comprobarCampos(nombreCampo,tipoValorCampo)) return 0;

        
    //Son dibujados en la pila de campos
    dibujarCampo(nombreCampo,tipoValorCampo);

    //Añadimos evento de eliminar
    var id = "eliminar-"+ contador;
    document.getElementById(id).addEventListener("click",eliminarCampo);
    contador = contador + 1;


    //Escritos dentro de los inputs hidden
    nombreCampoHidden = document.getElementById("id_nombre_campo");
    tipoValorCampoHidden = document.getElementById("id_tipo_valor");


    
    listaNombres.push(nombreCampo);
    listaTipos.push(tipoValorCampo);

    console.log("----agregados----");
    console.log(listaNombres);
    console.log(listaTipos);


    nombreCampoHidden.value = listaNombres.toString();
    tipoValorCampoHidden.value = listaTipos.toString();


    console.log(nombreCampoHidden.value);
    console.log(tipoValorCampoHidden.value);

    limpiarForm();

}

function eliminarCampo(e){
    //Removerlo de la pila de campos
    var elementoNombre = e.currentTarget.firstChild.innerText;
    var elementoTipo = e.currentTarget.children[1].innerText

    var campoEliminar = document.getElementById(e.currentTarget.id);
    
    contenedorCampos.removeChild(campoEliminar);

    //Removerlo de los values de nombreCampoHidden.value y tipoValorCampoHidden.value
    /*
    var listaNombresAux = nombreCampoHidden.value.split(",");
    if(listaNombresAux[listaNombresAux.length-1] == "")listaNombresAux.pop();

    var listaTiposAux = tipoValorCampoHidden.value.split(",");
    if(listaTiposAux[listaTiposAux.length-1]=="")listaTiposAux.pop();
    */
    
    console.log("---slice---")
    var index = remove(listaNombres,elementoNombre);
    removeTipos(listaTipos,elementoTipo, index);
    //listaTipos.splice(listaNombres.indexOf(elemento),1);
    console.log(listaNombres);
    console.log(listaTipos);
    nombreCampoHidden.value = listaNombres.toString();
    tipoValorCampoHidden.value = listaTipos.toString();
    console.log(nombreCampoHidden.value);
    console.log(tipoValorCampoHidden.value);



}

function remove(array, element) {
    var index = array.indexOf(element);
    
    if (index != -1) {
        array.splice(index, 1);
    }

    return index;
}


function removeTipos(array,element,index){
    if(index != -1){
        array.splice(index,1);
    }
}

function limpiarForm(){
    document.getElementById("id_nombre_de_campo_js").value = "";
    document.getElementById("id_tipo_valor_js").value = "";
}