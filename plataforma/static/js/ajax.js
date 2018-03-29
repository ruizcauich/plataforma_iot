/* 
 * Nombre del archivo: ajax.js
 * Descripción: Codigo del método gemérico que para usar ajax en cualquier
 *               parte de la aplicacion que lo necesite.
 * Autor (es): Augusto Neftalí Ruiz Cauich
 * Fecha de realización: 06-Diciembre-2017
 */

// recibe la url, los parámetros sin '?', el método a usar ('GET', 'POST'), y la función
// que se ejecutará al momento de recibir respuesta del servidor
function ejecutarAjax( url, parametros, metodo, callback){
    var objetoAjax =  new XMLHttpRequest();
    
    objetoAjax.onreadystatechange =  function(){
        if (this.readyState == 4 && this.status == 200) callback(this);
    };
    
    
    if( metodo == 'POST'){
        objetoAjax.open(metodo, url, true);
        //objetoAjax.setRequestHeader("Content-type", "multipart/form-data");
        objetoAjax.send( parametros );
    }else if( metodo == "GET" ){
        objetoAjax.open( metodo, url + "?"+ parametros, true);
        objetoAjax.send();
    }
    
    
}