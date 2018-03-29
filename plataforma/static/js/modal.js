
let disparadoresModal
let modales;
let cerradoresModal

LIBRERIA.Modal = function(id, padre){
        
    this.elemento = document.getElementById(id);
    if(this.elemento==null){
        this.elemento = document.createElement("div");
        this.elemento.setAttribute("id", id);
        this.elemento.setAttribute("class", "modal");

        this.dialogo = document.createElement("div");
        this.dialogo.setAttribute("class", "dialogo-modal");

        this.encabezado = document.createElement("div");
        this.encabezado.setAttribute("class", "encabezado-modal");
        this.cuerpo = document.createElement("div");
        this.cuerpo.setAttribute("class", "cuerpo-modal");
        this.pie = document.createElement("div");
        this.pie.setAttribute("class", "pie-modal");

        this.dialogo.appendChild(this.encabezado);
        this.dialogo.appendChild(this.cuerpo);
        this.dialogo.appendChild(this.pie);
        
        this.elemento.appendChild(this.dialogo);

        if(padre){
            document.getElementById(padre).appendChild(this.elemento);
        }
        else{
            document.body.appendChild(this.elemento);
        }

        


    }
    else{
        this.dialogo = this.elemento.children[0];
        this.encabezado = this.dialogo.querySelector("[class=encabezado-modal]")
        this.pie = this.dialogo.querySelector("[class=pie-modal]")
        this.cuerpo = this.dialogo.querySelector("[class=cuerpo-modal]")
    }
    initModales();

    this.abrir=function(padre){
        this.elemento.style.display="block";            
    }
    this.cerrar=function(){
        this.elemento.style.display="none";
    }
    
    this.reducido = ()=>{this.dialogo.setAttribute("class", "dialogo-modal-reducido");}
    this.grande =   ()=>{this.dialogo.setAttribute("class", "dialogo-modal");}
    this.peligro = ()=>{this.elemento.classList.add("peligro")}
    this.exito = ()=>{this.elemento.classList.add("exito")}
    this.informacion = ()=>{this.elemento.classList.add("informacion")}
    this.advertencia = ()=>{this.elemento.classList.add("advertencia")}
    
}

function initModales(){
    disparadoresModal = document.querySelectorAll("[data-trigger=abrir-modal]");
    // convierte NodeList a lista
    disparadoresModal = [].slice.call(disparadoresModal);
    disparadoresModal.forEach(elemento => {
        elemento.addEventListener("click", controladorModal)
    });

    cerradoresModal = document.querySelectorAll("[data-trigger=cerrar-modal]");
    cerradoresModal = [].slice.call(cerradoresModal);
    cerradoresModal.forEach(elemento => {
        elemento.addEventListener("click", cerrarModal)
    });

    modales = document.getElementsByClassName("modal");
    modales = [].slice.call(modales);
    modales.forEach(modal=>{
        modal.addEventListener("click", function(evento){
            if( !modales.includes(evento.target ))
                return;
            evento.target.style.display="none";
        })
    });

}


function controladorModal(evento){
    var modal = document.getElementById(evento.target.dataset["target"])
    modal.style.display = "block";
}


function cerrarModal(evento){
    var target = evento.target.dataset["target"];
    var modal = document.getElementById(target);
    modal.style.display = "none";
}

initModales();