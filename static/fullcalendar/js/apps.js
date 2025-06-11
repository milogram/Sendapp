document.addEventListener('DOMContentLoaded', function() {
    let calendarEl = document.getElementById('calendar');
    let frm = document.getElementById('formulario');
    const today = new Date().toLocaleDateString('en-CA'); // Obtén la fecha actual en formato local
    let eliminar = document.getElementById('btnEliminar');
    let myModal = new bootstrap.Modal(document.getElementById('myModal'));

    let calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        locale: 'es',
        headerToolbar: {
            left: 'prev next today',
            center: 'title',
            right: 'dayGridMonth timeGridWeek listWeek'
        },
        events: '/listar/',  // Ruta a tu vista de Django
        editable: true,

        dateClick: function (info) {
          
            if (info.dateStr >= today) {
                  // La fecha es válida, continúa con el proceso normal
                  frm.reset();
                  eliminar.classList.add('d-none');
                  document.getElementById('start').value = info.dateStr;
                  document.getElementById('start').value = info.dateStr;
                  document.getElementById('id').value = '';
                  document.getElementById('btnAccion').textContent = 'Registrar';
                  document.getElementById('titulo').textContent = 'Registrar Evento / Cita';
                  myModal.show();
               
            } else {
                Swal.fire(
                    'Aviso',
                    'No puedes seleccionar fechas anterios a la actual',
                    'warning'
                );
            }
        },
        
        eventAllow: function (dropInfo) {
            return dropInfo.startStr >= today;
        },


        eventClick: function (info) {
            document.getElementById('id').value = info.event.id;
            document.getElementById('tipo').value = info.event.extendedProps.tipo;  // Agregar esta línea
            document.getElementById('title').value = info.event.title;
            document.getElementById('start').value = info.event.startStr;
            document.getElementById('time').value = info.event.extendedProps.time; 
            document.getElementById('description').value = info.event.extendedProps.description;
            document.getElementById('color').value = info.event.backgroundColor;

            document.getElementById('btnAccion').textContent = 'Modificar';
            document.getElementById('titulo').textContent = 'Actualizar Evento / Cita';
            eliminar.classList.remove('d-none');
            myModal.show();
        },
        
        eventDrop: function (info) {
            const start = info.event.startStr;
            const id = info.event.id;
            const url = '/drag/'; 

            const data = {
                start: start,
                id: id
            };

            $.ajax({
                type: "POST",
                url: url,
                data: data,
                success: function (data) {
                    console.log(data);
                    Swal.fire(
                        'Avisos?',
                        data.msg,
                        data.tipo
                    );
                    if (data.estado) {
                        myModal.hide();
                        calendar.refetchEvents();
                    }
                },
                error: function (error) {
                    console.error(error);
                    Swal.fire(
                        'Avisos?',
                        'Hubo un error al arrastrar el evento',
                        'error'
                    );
                }
            });
        }
    });

    calendar.render();

   

    frm.addEventListener('submit', function (e) {
        e.preventDefault();
        const tipo = document.getElementById('tipo').value;        
        const start = document.getElementById('start').value;
        const time = document.getElementById('time').value;
        const description = document.getElementById('description').value;
        const color = document.getElementById('color').value;


        
        if ( tipo == '' || title == '' || start == '' || time == '' || description == '' || color == "") {
            Swal.fire(
                'Avisos',
                'Todos los campos son obligatorios',
                'warning'
            );
        } else {
            const formData = $(frm).serialize();

            $.ajax({
                type: "POST",
                url: '/registrar/',  
                data: formData,
                success: function(data) {
                    console.log(data);
                    Swal.fire(
                        'Avisos?',
                        'Registro realizado con éxito',
                        'success'
                    );
                    myModal.hide();
                    calendar.refetchEvents();
                },
                error: function(error) {
                    console.error(error);
                    Swal.fire(
                        'Avisos?',
                        'Hubo un error en la solicitud POST.',
                        'error'
                    );
                }
            });
        }
    });

    eliminar.addEventListener('click', function () {
        myModal.hide();
        Swal.fire({
            title: 'Advertencia?',
            text: "¿Está seguro de eliminar?",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, eliminar'
        }).then((result) => {
            if (result.isConfirmed) {
                const eventId = document.getElementById('id').value;
                const url = '/eliminar/' + eventId;  
                $.ajax({
                    type: "GET",
                    url: url,
                    success: function (data) {
                        console.log(data);
                        Swal.fire(
                            'Avisos?',
                            data.msg,
                            data.tipo
                        );
                        if (data.estado) {
                            calendar.refetchEvents();
                        }
                    },
                    error: function (error) {
                        console.error(error);
                        Swal.fire(
                            'Avisos?',
                            'Hubo un error al eliminar el evento',
                            'error'
                        );
                    }
                });
            }
        });
    });
});
