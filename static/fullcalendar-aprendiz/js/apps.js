let calendarEl = document.getElementById('calendar');
let frm = document.getElementById('formulario');
let myModal = new bootstrap.Modal(document.getElementById('myModal'));
document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var usuarioId = new URLSearchParams(window.location.search).get('usuario_id'); // Obtener el usuario_id de la URL

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'es',
        headerToolbar: {
            left: 'prev next today',
            center: 'title',
            right: 'dayGridMonth timeGridWeek listWeek'
        },
        eventSources: [
            {
                url: '/ver_calendario_usuario/' + usuarioId + '/',
                method: 'GET'
            }
        ],
        editable: true,
      
 
        eventClick: function (info) {
          document.getElementById('id').value = info.event.id;
          document.getElementById('title').value = info.event.title;
          document.getElementById('start').value = info.event.startStr;
          document.getElementById('time').value = info.event.extendedProps.time; 
          document.getElementById('description').value = info.event.extendedProps.description; // Agrega esta línea para el campo de descripción
          document.getElementById('titulo').textContent = 'Detalles del Evento';

          // Deshabilitar la edición de campos
          document.getElementById('title').readOnly = true;
          document.getElementById('start').readOnly = true;
          document.getElementById('time').readOnly = true;
          document.getElementById('description').readOnly = true;

          console.log(info.event.title, info.event.extendedProps.description)

          myModal.show();
      },
      
    });
    calendar.render();
   
  

})