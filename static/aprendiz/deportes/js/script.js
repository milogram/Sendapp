//menu
//Ejecutar funcion en el evento click
document.getElementById("btn_abrir").addEventListener("click", open_close_menu);
//Declaramos variables
var side_menu = document.getElementById("menu");
var btn_open = document.getElementById("btn_abrir");
var body = document.getElementById("body");

//Funcion para mostrar y ocultar menu
function open_close_menu(){
    body.classList.toggle("body_move");
    side_menu.classList.toggle("menu_move");
}

//Si el ancho de la pagina es menor a 760px ocultara el menu
if(window.innerWidth < 760){
    body.classList.add("body_move");
    side_menu.classList.add("menu_move");
}

//menu responsive
window.addEventListener("resize", function(){
    if (this.window.innerWidth > 760){
        body.classList.remove("body_move");
        side_menu.classList.remove("menu_move");
    }else{
        body.classList.add("body_move");
        side_menu.classList.add("menu_move");
    }
});
