from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from sendapp import views


urlpatterns = [
   
    #Aprendiz
    path('home/', views.home, name='home'),
    path('deportes/', views.deportes, name='deportes'),
    path('psicosocial/', views.psicosocial, name='psicosocial'),
    path('enfermeria/', views.enfermeria, name='enfermeria'),
    path('arte/', views.arte, name='arte'),
    path('administrativo/', views.administrativo, name='administrativo'),
    path('sostenimiento/', views.sostenimiento, name='sostenimiento'),
    path('liderazgo/', views.liderazgo, name='liderazgo'),
    path('agendar_cita/', views.agendar_cita, name='agendar_cita'),


    #Ingreso
    path('', views.ingreso, name='ingreso'),
    path('ingresar/', views.ingresar, name='ingresar'),
    path('register/', views.añadir, name='añadir'),
    path('cerrar/', views.cerrar, name='cerrar'),
    path('olvidar/', views.restablecer_contrasena, name='olvidar'),


    #calendario
    path('calendario/', views.calendar, name='calendario'),
    path('registrar/', views.registrar, name='registrar'),
    path('listar/', views.listar, name='listar'),
    path('eliminar/<int:id>/', views.eliminar, name='eliminar'),
    path('drag/', views.drag, name='drag'),

    #calendario publico
    path('calendario-aprendiz/', views.calendar_aprendiz, name='calendario-aprendiz'),
    path('ver_calendario_usuario/<int:usuario_id>/', views.listar_eventos_usuario, name='ver_calendario_usuario'),
   
    #usuario bienestar
    path('bienestar', views.inicio_bienestar, name='bienestar'),
    path('listar_solicitudes/', views.listar_solicitudes, name='listar_solicitudes'),
    path('aceptar_solicitud/<int:solicitud_id>/', views.aceptar_solicitud, name='aceptar_solicitud'),
    path('confirmar_cita/<int:solicitud_id>/', views.confirmar_cita, name='confirmar_cita'),
    path('rechazar_solicitud/<int:solicitud_id>/', views.rechazar_solicitud, name='rechazar_solicitud'),

    #usuario admninistrador
    path('administrador', views.inicio_admin, name='admin'),
    path('get_user_list/', views.get_user_list, name='get_user_list'),
    path('editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),

    #perfil
    path('perfil/<int:usuario_id>/', views.perfil, name='perfil'),
    path('perfil/modificar/<int:usuario_id>/', views.modificar_perfil, name='modificar_perfil'),

    #perfil_admin
    path('perfil_admin/<int:usuario_id>/', views.perfil_admin, name='perfil_ad'),
    path('perfil/modificar_admin/<int:usuario_id>/', views.modificar_perfil_admin, name='modificar_perfil_ad'),

]
