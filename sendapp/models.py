from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils import timezone


class UsuarioManager(BaseUserManager):
    def crear_usuario(self, nombre_usuario, apellido_usuario, telefono_usuario, id_area, correo_usuario, id_rol, cedula, password=None):
        if not cedula:
            raise ValueError('La cédula es obligatoria.')
        usuario = self.model(nombre_usuario=nombre_usuario,apellido_usuario = apellido_usuario,
                             correo_usuario=correo_usuario, telefono_usuario = telefono_usuario, id_area=id_area, id_rol=id_rol, cedula=cedula)
        usuario.set_password(password)  # Utiliza set_password para almacenar la contraseña de forma segura
        usuario.save(using=self._db)
        return usuario
    
    def create_superuser(self, cedula, password=None):
    # Obtén el rol con id_2
        try:
            rol = Rol.objects.get(id_rol=2)
        except Rol.DoesNotExist:
            raise Exception('El rol con id_2 no existe en la base de datos.')

        try:
            area = Area.objects.get(id_area=1)
        except Area.DoesNotExist:
            raise Exception('El area con id_1 no existe en la base de datos.')

        usuario = self.crear_usuario(

            nombre_usuario='',
            apellido_usuario='',
            telefono_usuario='',
            id_area=area,
            correo_usuario='',
            cedula=cedula,
            password=password,
            id_rol=rol  # Asigna el rol al superusuario
        )
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.save(using=self._db)
        return usuario


# Define el modelo para el rol
class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_rol  # Esto mostrará el nombre del área

# Define el modelo para el area
class Area(models.Model):
    id_area = models.AutoField(primary_key=True)
    nombre_area = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre_area  # Esto mostrará el nombre del área

# Define el modelo para el usuario
class Usuario(AbstractBaseUser,PermissionsMixin):
    cedula = models.CharField(max_length=15, unique=True)
    nombre_usuario = models.CharField(max_length=30)
    apellido_usuario = models.CharField(max_length=30)
    telefono_usuario = models.CharField(max_length=20)
    correo_usuario = models.EmailField()
    id_area = models.ForeignKey(Area, on_delete=models.CASCADE)
    id_rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager() #se asigna el gestor de usuario

    USERNAME_FIELD = 'cedula' 

    def __str__(self):
        return f'{self.nombre_usuario} {self.apellido_usuario} ({self.cedula})'
    
class Evento(models.Model):
    TIPO_CHOICES = (
        ('evento', 'Evento'),
        ('cita', 'Cita'),
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Agregar esta línea
    title = models.CharField(max_length=255)
    start = models.DateField()
    time = models.TimeField()
    description = models.CharField(max_length=500)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.title
    
    
class EventoModel:
    def registrar(self, title, inicio, time, description, color):
        evento = Evento(title=title, start=inicio, time=time, description=description, color=color)
        evento.save()

    def getEventos(self):
        eventos = Evento.objects.all()
        return eventos

    def modificar(self, title, inicio, color, id):
        try:
            evento = Evento.objects.get(id=id)
            evento.title = title
            evento.start = inicio
            evento.color = color
            evento.save()
        except Evento.DoesNotExist:
            pass

    def eliminar(self, id):
        try:
            evento = Evento.objects.get(id=id)
            evento.delete()
        except Evento.DoesNotExist:
            pass

    def dragOver(self, start, id):
        try:
            evento = Evento.objects.get(id=id)
            evento.start = start
            evento.save()
        except Evento.DoesNotExist:
            pass

#modelos_cita
class SolicitudCita(models.Model):

    area = models.ForeignKey(Area, on_delete=models.CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField() 
    fecha_cita = models.DateField(null=True, blank=True) # Nuevo campo
    hora_cita = models.TimeField(null=True, blank=True)
    ficha = models.CharField(max_length=10)
    descripcion = models.TextField(max_length=500)

    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    )
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    
    def __str__(self):
        return f'{self.nombre} {self.apellidos} - {self.fecha_cita} {self.hora_cita}'