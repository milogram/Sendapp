from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario, Evento, Rol, Area, SolicitudCita

admin.site.register(Evento)
admin.site.register(Rol)
admin.site.register(Area)
admin.site.register(SolicitudCita)
admin.site.register(Usuario)