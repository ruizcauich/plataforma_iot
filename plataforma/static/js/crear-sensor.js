window.onload = inicio;

function inicio(){
    document.getElementById("id_nombre_campo").value = "";
    document.getElementById("id_tipo_valor").value = "";
    document.getElementById("id_nombre_de_campo_js").value = "";
    document.getElementById("id_tipo_valor_js").value = "";
    document.getElementById("id_nombre_de_sensor").value = "";
    document.getElementById("id_tipo").value = "";
}

function agregarCampo(){

    //Obtención de los datos del campo
    var nombreCampo = document.getElementById("id_nombre_de_campo_js").value;
    var tipoValorCampo = document.getElementById("id_tipo_valor_js").value;

    //Son dibujados en la pila de campos
    nuevoCampo = document.createElement("div");
    nuevoCampoNombre = document.createElement("h3");
    contenedorCampos = document.getElementById("campos");
    nuevoCampo.className = "campo";
    nuevoCampoNombreContent = document.createTextNode(nombreCampo);
    nuevoCampoNombre.appendChild(nuevoCampoNombreContent);
    nuevoCampo.appendChild(nuevoCampoNombre);
    contenedorCampos.appendChild(nuevoCampo);

    //Escritos dentro de los inputs hidden
    var nombreCampoHidden = document.getElementById("id_nombre_campo");
    var tipoValorCampoHidden = document.getElementById("id_tipo_valor");

    nombreCampoHidden.value += nombreCampo +",";
    tipoValorCampoHidden.value += tipoValorCampo + ",";

    console.log(nombreCampoHidden.value)
    console.log(tipoValorCampoHidden.value)

    limpiarForm()

}

function limpiarForm(){
    document.getElementById("id_nombre_de_campo_js").value = "";
    document.getElementById("id_tipo_valor_js").value = "";
}