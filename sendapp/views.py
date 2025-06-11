from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Usuario, Rol, Evento, SolicitudCita, Area
from .forms import UsuarioForm, SolicitudCitaForm, ModificarPerfilForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponse
from django.contrib import messages
from django.db.utils import IntegrityError
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.utils import timezone
import locale, secrets, random, string

from django.conf import settings

User = get_user_model()

#ingreso
def ingreso(request):
    return render(request, 'registration/seleccion.html')

def ingresar(request):
    if request.method == 'POST':
        cedula = request.POST['cedula']
        password = request.POST['password']

        user = authenticate(request, cedula=cedula, password=password)

        if user is not None:
            login(request, user)
            user_rol = user.id_rol  # Obtiene el rol del usuario autenticado

            # Ahora, puedes redirigir al usuario según su rol
            if user_rol.id_rol == 1:
               
                return redirect('bienestar')  # Redirige a la interfaz de Bienestar
            elif user_rol.id_rol == 2:
                return redirect('admin')  # Redirige a la interfaz de Administrador
            
        else:
            # verifica  si la cédula es válida pero la contraseña es incorrecta
            user_by_cedula = Usuario.objects.filter(cedula=cedula).first()
            if user_by_cedula:
                error = 'Contraseña incorrecta'
            else:
                error = 'El usuario no existe'
                
            return render(request, 'registration/login.html', {"msj_error": error})
    
    return render(request, 'registration/login.html')

#olvide contraseña
def restablecer_contrasena(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        usuario = User.objects.filter(cedula=cedula).first()

        if usuario:
            # Genera una contraseña temporal
            temp_password = secrets.token_urlsafe(8)

            # Cambia automáticamente la contraseña del usuario por la contraseña temporal
            usuario.set_password(temp_password)
            usuario.save()

            # Envia el correo electrónico con la contraseña temporal y el mensaje
            subject = 'Restablecimiento de Contraseña'
            message = f'Tu nueva contraseña temporal es: {temp_password}\nRecuerda cambiarla al iniciar sesión.'
            from_email = 'useraprendiz3@gmail.com'  # Cambia por tu correo electrónico
            to_email = usuario.correo_usuario

            send_mail(subject, message, from_email, [to_email])

            messages.success(request, 'Se ha enviado un correo electrónico con las instrucciones para restablecer la contraseña.')
            return redirect('ingresar')

        else:
            messages.error(request, 'El usuario con la cédula proporcionada no existe.')

    return render(request, 'registration/restablecer.html')

@login_required #Requiere que este logueado
def cerrar(request):
    logout(request)
    return redirect('ingreso')
    

@login_required #Requiere que este logueado
def añadir(request):
    if request.method == 'POST':
        # Obtiene los datos de los campos del formulario
        nombres = request.POST['nombres']
        apellidos = request.POST['apellidos']
        correo = request.POST['correo']
        telefono = request.POST['telefono']
        cedula = request.POST['cedula']
        password = request.POST['password']
        id_area = request.POST['area']
        id_rol = request.POST['rol']

        try:
            # Intenta obtener el objeto Rol y Area
            rol = Rol.objects.get(id_rol=id_rol)
            area = Area.objects.get(id_area=id_area)

            # Intenta crear el usuario
            user = Usuario.objects.crear_usuario(
                nombre_usuario=nombres, 
                apellido_usuario=apellidos, 
                correo_usuario=correo, 
                id_area=area,  # Cambia id_area al objeto Area
                telefono_usuario=telefono, 
                cedula=cedula, 
                password=password, 
                id_rol=rol
            )
           

            # Agregar un mensaje de éxito
            messages.success(request, 'El registro se realizó exitosamente.')
            
            return render(request, 'registration/registrar.html')
        
        except IntegrityError:
            # Captura la excepción si la cédula ya existe
            messages.error(request, 'La cédula ya está registrada. Intente con otra.')
            return render(request, 'registration/registrar.html')

    # Si la solicitud no es POST, redirige a la página de registro
    return render(request, 'registration/registrar.html')


#administrador
@login_required #Requiere que este logueado
def inicio_admin(request):
    usuario_actual = request.user # Obtén el usuario autenticado actual

    return render(request, 'administrador/index.html', {
        'usuario_actual': usuario_actual,
    })  

@login_required #Requiere que este logueado
def get_user_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'administrador/user_list_partial.html', {'usuarios': usuarios})


#editar usuarios
@login_required #
def editar_usuario(request, usuario_id):
    usuario = Usuario.objects.get(pk=usuario_id)

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        
        if form.is_valid():
            usuario.nombre_usuario = form.cleaned_data['nombres']
            usuario.apellido_usuario = form.cleaned_data['apellidos']
            usuario.correo_usuario = form.cleaned_data['correo']
            usuario.telefono_usuario = form.cleaned_data['telefono']
            id_area = form.cleaned_data['area']
            area = get_object_or_404(Area, pk=id_area)
            usuario.id_area = area
            usuario.cedula = form.cleaned_data['cedula']
            usuario.save()

            # Mensaje de éxito
            messages.success(request, 'Usuario actualizado correctamente.')
        else:
            # Mensaje de error si el formulario no es válido
            messages.error(request, 'Error en el formulario. Por favor, corrige los errores.')
    else:
        form = UsuarioForm(initial={
            'nombres': usuario.nombre_usuario,
            'apellidos': usuario.apellido_usuario,
            'correo': usuario.correo_usuario,
            'telefono': usuario.telefono_usuario,
            'area': usuario.id_area.pk,
            'rol': usuario.id_rol,
            'cedula': usuario.cedula,
        })

    return render(request, 'administrador/editar.html', {'form': form})

#Bienestar
@login_required #Requiere que este logueado
def inicio_bienestar(request):
    usuario_actual = request.user # Obtén el usuario autenticado actual

    return render(request, 'bienestar/index.html', {
        'usuario_actual': usuario_actual,
    })  # 'index.html' es el nombre de tu plantilla



#Calendario vista administradores
@login_required #Requiere que este logueado
def calendar(request):
    return render(request,'calendario/base.html')

@csrf_exempt
def registrar(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        title = request.POST.get('title')
        start = request.POST.get('start')
        time = request.POST.get('time')
        description = request.POST.get('description')
        color = request.POST.get('color')
        tipo = request.POST.get('tipo')  # Agrega esta línea para obtener el tipo del evento
        user = request.user  # Asignar el evento al usuario actual

        if not title or not start or not tipo:  # Asegúrate de que el tipo también esté presente
            msg = {'msg': 'Todos los campos son obligatorios', 'estado': False, 'tipo': 'warning'}
        else:
            if not id:
                # Crear un nuevo evento
                event = Evento(title=title, start=start, time=time, description=description, color=color, tipo=tipo, user=user)
                event.save()
                msg = {'msg': 'Evento Registrado', 'estado': True, 'tipo': 'success'}
            else:
                try:
                    event = Evento.objects.get(id=id)

                    # Actualizar solo los campos que se proporcionaron en la solicitud
                    event.title = title
                    event.start = start
                    event.time = time
                    event.description = description
                    event.color = color
                    event.tipo = tipo  # Actualiza el tipo del evento

                    event.save()
                  
                    msg = {'msg': 'Evento Modificado', 'estado': True, 'tipo': 'success'}
                except Evento.DoesNotExist:
                    return JsonResponse({'msg': 'Evento no encontrado', 'estado': False, 'tipo': 'danger'})

        return JsonResponse(msg)

    return JsonResponse({'msg': 'Método no permitido', 'estado': False, 'tipo': 'danger'})




def listar(request):
    if request.user.id_rol.id_rol == 2:  # El usuario es un administrador
        data = Evento.objects.all().values()
    elif request.user.id_rol.id_rol == 1:  # El usuario es un usuario normal
        data = Evento.objects.filter(user=request.user).values()  # Cambia 'usuario' a 'user'
    else:
        return HttpResponseForbidden("No tienes permiso para ver esta página.")
    return JsonResponse(list(data), safe=False)


def eliminar(request, id):
    try:
        evento = Evento.objects.get(id=id)
        evento.delete()
        msg = {'msg': 'Evento Eliminado', 'estado': True, 'tipo': 'success'}
    except Evento.DoesNotExist:
        msg = {'msg': 'Evento no encontrado', 'estado': False, 'tipo': 'danger'}
    except Exception as e:
        msg = {'msg': f'Error al Eliminar: {str(e)}', 'estado': False, 'tipo': 'danger'}

    return JsonResponse(msg)


@csrf_exempt
def drag(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        start = request.POST.get('start')

        if not (id and start):
            return JsonResponse({'msg': 'Todo los campos son requeridos', 'estado': False, 'tipo': 'danger'})

        event = Evento.objects.get(id=id)
        event.start = start
        event.save()
        return JsonResponse({'msg': 'Evento Modificado', 'estado': True, 'tipo': 'success'})


#calendario publico
def calendar_aprendiz(request):
    usuario_id = request.GET.get('usuario_id', None)  # Obtener el usuario_id de la consulta
    if usuario_id is not None:
        return render(request, 'calendario/calendario_aprendiz.html', {'usuario_id': usuario_id})
    else:
        return HttpResponse("Usuario no especificado")
        
def listar_eventos_usuario(request, usuario_id):
    try:
        eventos = Evento.objects.filter(user_id=usuario_id, tipo='evento').values()
        # Aquí, filtramos los eventos por el ID del usuario específico
        return JsonResponse(list(eventos), safe=False)
    except Evento.DoesNotExist:
        return HttpResponseNotFound("Usuario no encontrado o no tiene eventos programados.")

#perfil
@login_required #Requiere que este logueado
def perfil(request, usuario_id):
   
    usuario_actual = get_object_or_404(Usuario, id=usuario_id)

    context = {
        'usuario_actual': usuario_actual,
    }

    return render(request, 'perfil/perfil.html', context)


from django.contrib.auth import update_session_auth_hash

@login_required
def modificar_perfil(request, usuario_id):
    show_success_message = ""
    show_error_message = ""
    show_no_change_message = ""
    usuario_actual = get_object_or_404(Usuario, id=usuario_id)

    if request.user != usuario_actual:
        messages.error(request, 'No tienes permiso para modificar este perfil.')
        return redirect('perfil', usuario_id=usuario_id)

    if request.method == 'POST':
        form = ModificarPerfilForm(request.POST, instance=usuario_actual)
        if form.is_valid():
            new_username = form.cleaned_data['new_username']
            new_password = form.cleaned_data['new_password']
            confirmar_password = form.cleaned_data['confirmar_password']

            if new_password and confirmar_password and new_password != confirmar_password:
                show_error_message = "Las contraseñas no coinciden. Los cambios no se guardaron."

            elif (new_password and not confirmar_password) or (not new_password and confirmar_password):
                    show_error_message = "Completa ambos campos de contraseña."
            else:
                if new_username != usuario_actual.nombre_usuario or new_password:
                    user = form.save(commit=False)

                    if new_password:
                        user.password = make_password(new_password)
                        update_session_auth_hash(request, user)

                    if new_username:
                        user.nombre_usuario = new_username

                    user.save()
                    show_success_message = 'Perfil modificado con éxito.'
                else:
                    show_no_change_message = 'No se detectaron cambios en el perfil.'
        else:
            show_error_message = "Hubo un error al modificar el perfil. Por favor, revisa los datos ingresados."

    else:
        initial_data = {'new_username': usuario_actual.nombre_usuario}
        form = ModificarPerfilForm(instance=usuario_actual, initial=initial_data)

    return render(request, 'perfil/modificar_perfil.html', {'form': form, 'usuario_actual': usuario_actual, 'error_message': show_error_message, 'success_message': show_success_message, 'no_change_message': show_no_change_message})

@login_required #Requiere que este logueado
def perfil_admin(request, usuario_id):
   
    usuario_actual = get_object_or_404(Usuario, id=usuario_id)

    context = {
        'usuario_actual': usuario_actual,
    }

    return render(request, 'perfil_admin/perfil.html', context)

@login_required #Requiere que este logueado
def modificar_perfil_admin(request, usuario_id):
    show_success_message = ""
    show_error_message = ""
    show_no_change_message = ""
    usuario_actual = get_object_or_404(Usuario, id=usuario_id)

    if request.user != usuario_actual:
        messages.error(request, 'No tienes permiso para modificar este perfil.')
        return redirect('perfil', usuario_id=usuario_id)

    if request.method == 'POST':
        form = ModificarPerfilForm(request.POST, instance=usuario_actual)
        if form.is_valid():
            new_username = form.cleaned_data['new_username']
            new_password = form.cleaned_data['new_password']
            confirmar_password = form.cleaned_data['confirmar_password']

            if new_password and confirmar_password and new_password != confirmar_password:
                show_error_message = "Las contraseñas no coinciden. Los cambios no se guardaron."

            elif (new_password and not confirmar_password) or (not new_password and confirmar_password):
                    show_error_message = "Completa ambos campos de contraseña."
            else:
                if new_username != usuario_actual.nombre_usuario or new_password:
                    user = form.save(commit=False)

                    if new_password:
                        user.password = make_password(new_password)
                        update_session_auth_hash(request, user)

                    if new_username:
                        user.nombre_usuario = new_username

                    user.save()
                    show_success_message = 'Perfil modificado con éxito.'
                else:
                    show_no_change_message = 'No se detectaron cambios en el perfil.'
        else:
            show_error_message = "Hubo un error al modificar el perfil. Por favor, revisa los datos ingresados."

    else:
        initial_data = {'new_username': usuario_actual.nombre_usuario}
        form = ModificarPerfilForm(instance=usuario_actual, initial=initial_data)

    return render(request, 'perfil_admin/modificar_perfil.html', {'form': form, 'usuario_actual': usuario_actual, 'error_message': show_error_message, 'success_message': show_success_message, 'no_change_message': show_no_change_message})

#Corresponde a la vista de agendamiento de citas por parte del aprendiz.
def agendar_cita(request):
    mensaje_exito = None
    mensaje_error = None

    if request.method == 'POST':
        form = SolicitudCitaForm(request.POST)
        
        if form.is_valid():
            solicitud = form.save(commit=False)

            # Obtiene todos los usuarios asociados al área seleccionada
            area = solicitud.area
            usuarios = Usuario.objects.filter(id_area=area)

            if usuarios.exists():
                # Itera sobre todos los usuarios y crea una solicitud para cada uno
                for usuario in usuarios:
                    solicitud = form.save(commit=False)
                    solicitud.usuario = usuario
                    solicitud.estado = 'pendiente'  # Establece el estado como "pendiente"
                    solicitud.save()
                    
                    # Enviar correo electrónico al usuario del área
                    subject = 'Nueva Solicitud de Cita'
                    message = f'Nueva solicitud de cita en SENDAPP, en el área de {area.nombre_area}. Descripción: {solicitud.descripcion}'
                    from_email = settings.DEFAULT_FROM_EMAIL  # Utiliza la configuración predeterminada de correo electrónico
                    to_email = usuario.correo_usuario  # Correo del usuario del área

                    send_mail(subject, message, from_email, [to_email])

                mensaje_exito = 'La cita fue agendada correctamente.'
            else:
                mensaje_error = 'No se encontraron usuarios asociados al área seleccionada.'
        else:
            mensaje_error = 'Por favor, corrija los errores en el formulario.'
    else:
        form = SolicitudCitaForm()

    return render(request, 'aprendiz/agendar_cita.html', {'form': form, 'mensaje_exito': mensaje_exito, 'mensaje_error': mensaje_error})

@login_required
def listar_solicitudes(request):
    # Obtiene el usuario actualmente autenticado
    usuario = request.user

    # Filtra las solicitudes excluyendo las que tienen estado "rechazada" y que pertenecen al área del usuario
    solicitudes = SolicitudCita.objects.exclude(estado='rechazada').filter(area=usuario.id_area).all()
    
    return render(request, 'bienestar/solicitudes.html', {'solicitudes': solicitudes})

@login_required
def aceptar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudCita, id=solicitud_id)

    if solicitud.estado == 'pendiente':
       

        # Redirige a una nueva plantilla para ingresar fecha y hora
        return render(request, 'bienestar/fecha_hora.html', {'solicitud_id': solicitud.id})

    else:
        messages.error(request, 'No se puede aceptar una solicitud que no está en estado pendiente.')
        return redirect('confirmar_cita', solicitud_id=solicitud.id)
    
@login_required
def confirmar_cita(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudCita, id=solicitud_id)

    if request.method == 'POST':
        fecha_cita = request.POST.get('fecha_cita')
        hora_cita = request.POST.get('hora_cita')

        # Guarda la fecha y hora ingresadas
        solicitud.fecha_cita = fecha_cita
        solicitud.hora_cita = hora_cita
        solicitud.estado = 'aceptada'
        solicitud.save()
       
                

        # Convierte la fecha de cadena a objeto de fecha
        fecha_cita_obj = timezone.datetime.strptime(fecha_cita, '%Y-%m-%d').date()

        # Configura el idioma local a español
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

        # Obtiene el nombre del día en español
        nombre_dia = fecha_cita_obj.strftime('%A')

        # Restaura el idioma local al predeterminado
        locale.setlocale(locale.LC_TIME, '')

          # Crear evento en el calendario
        evento_cita = Evento(
            title= f"{solicitud.nombre} {solicitud.apellidos}",
            start= solicitud.fecha_cita,
            time= solicitud.hora_cita,
            description= solicitud.descripcion,
            color= generar_color_aleatorio(),
            user_id= solicitud.usuario_id ,
            tipo='cita',
        )
        evento_cita.save()

        # Enviar correo de confirmación con más información
        subject = 'Cita Confirmada'
        hora_am_pm = 'AM' if int(solicitud.hora_cita.split(':')[0]) < 12 else 'PM'
        message = f'Su cita con bienestar al aprendiz ha sido confirmada en el área de {solicitud.area.nombre_area} para el día {nombre_dia}, {solicitud.fecha_cita} a las {solicitud.hora_cita} {hora_am_pm}. ¡Esperamos su asistencia!'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = solicitud.email

        send_mail(subject, message, from_email, [to_email])

        messages.success(request, 'Cita confirmada con éxito.')
        return redirect('listar_solicitudes')

    return redirect('listar_solicitudes')

def generar_color_aleatorio():
    # Genera un color aleatorio en formato hexadecimal
    color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return color

@login_required #Requiere que este logueado
def rechazar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudCita, id=solicitud_id)

    if solicitud.estado == 'pendiente':  # Verifica que la solicitud esté en estado pendiente
        solicitud.estado = 'rechazada'
        solicitud.save()

        # Enviar correo de rechazo
        subject = 'Solicitud de Cita Rechazada'
        message = 'Lamentamos informarle que su solicitud de cita ha sido rechazada. Si tiene alguna pregunta, por favor contáctenos al [numero bienestar].'
        from_email = 'useraprendiz3@gmail.com'  # Cambia esto al correo desde el cual deseas enviar los mensajes
        to_email = solicitud.email

        send_mail(subject, message, from_email, [to_email])

        messages.success(request, 'Solicitud rechazada con éxito.')
    else:
        messages.error(request, 'No se puede rechazar una solicitud que no está en estado pendiente.')

    return redirect('listar_solicitudes')


#aprendiz
def home(request):
    return render(request, 'aprendiz/index.html')  # 'index.html' es el nombre de tu plantilla

def deportes(request):
    return render(request, 'aprendiz/deportes.html')


def psicosocial(request):
    return render(request, 'aprendiz/psicosocial.html')

def enfermeria(request):
    return render(request, 'aprendiz/enfermeria.html')


def arte(request):
    return render(request, 'aprendiz/arte.html')

def administrativo(request):
    return render(request, 'aprendiz/administrativo.html')


def sostenimiento(request):
    return render(request, 'aprendiz/sostenimiento.html')


def liderazgo(request):
    return render(request, 'aprendiz/liderazgo.html')



