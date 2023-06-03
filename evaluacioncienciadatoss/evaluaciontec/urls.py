from django.urls import path, re_path
#from django.conf.urls import url
from .views import index,backup#,check, respaldo 
from .views import departamento_upload,carrera_upload,evaluadepa_upload,maestros_upload
from .views import departamentos_download,carrera_download,evaluadepa_download,maestros_download
#evaluamaestro_download
from .views import DepartamentoList,DepartamentoCreate,DepartamentoUpdate,DepartamentoDelete
from .views import CarreraList,CarreraCreate,CarreraUpdate,CarreraDelete
from .views import MaestrosList,MaestrosCreate,MaestrosUpdate,MaestrosDelete
from .views import EvaluaDepartamentoList, EvaluaDepartamentoCreate,EvaluaDepartamentoUpdate,EvaluaDepartamentoDelete
from .views import ciencias_tierra, cienciasytierra, economia_administracion,economiayadministracion
from .views import sistemas_computacion, sistemasycomputacion, electrica_electronica,electricayelectronica
from .views import mecanica, mecanicaD, industrial,industrialD, ciencia_basica, ciencias_basicas, idioma, idiomas
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('',login_required(index)),
    path('respaldo', backup, name='backup'),    
    #path('respaldo',login_required(respaldo)),
    #path('check', check, name='check'),      #
    path('consultar_departamento',DepartamentoList.as_view(),name='ver_departamento'),
    path('añadir_departamento',login_required(DepartamentoCreate.as_view())),    
    re_path(r'^modificar_departamento/(?P<pk>\d+)/$',login_required(DepartamentoUpdate.as_view()), name= 'modi_departamento'),
    re_path(r'^eliminar/(?P<pk>\d+)/$',login_required(DepartamentoDelete.as_view()), name= 'eli_departamento'),
    path('departamento_download', departamentos_download,name='departamento_download'),
    path('upload',departamento_upload, name='upload'),
    #
    path('añadir_carrera',login_required(CarreraCreate.as_view())),
    path('consultar_carrera',login_required(CarreraList.as_view()),name='ver_carrera'),
    re_path(r'^modificar_carrera/(?P<pk>\d+)/$',login_required(CarreraUpdate.as_view()), name= 'modi_carrera'),
    re_path(r'^eliminar/(?P<pk>\d+)/$',login_required(CarreraDelete.as_view()), name= 'eli_carrera'),
    path('carrera_download', carrera_download, name='carrera_download'),
    path('upload',carrera_upload, name='upload'),
    #
    path('añadir_maestro',login_required(MaestrosCreate.as_view())),
    path('consultar_maestro',login_required(MaestrosList.as_view()),name='ver_maestro'),
    re_path(r'^modificar_maestro/(?P<pk>\d+)/$',login_required(MaestrosUpdate.as_view()), name= 'modi_maestro'),
    re_path(r'^eliminar/(?P<pk>\d+)/$',login_required(MaestrosDelete.as_view()), name= 'eli_maestro'),
    path('maestro_download',maestros_download, name='maestro_download'),
    path('subeMaestro',maestros_upload, name='upload'),
    #
    path('añadir_evaluadepartamento',login_required(EvaluaDepartamentoCreate.as_view())),
    path('consultar_evluadepartamento',login_required(EvaluaDepartamentoList.as_view()),name='ver_evaluadepartamento'),
    re_path(r'^modificar_evaluadepartamento/(?P<pk>\d+)/$',login_required(EvaluaDepartamentoUpdate.as_view()), name= 'modi_evaluadepartamento'),
    re_path(r'^eliminar_evluardepartamento/(?P<pk>\d+)/$',login_required(EvaluaDepartamentoDelete.as_view()), name= 'eli_evaluadepartamento'),
    path('estadisticas_download', evaluadepa_download, name='estadisticas_download'),
    path('subeEvaluaDepartamento',evaluadepa_upload, name='upload'),
    #
    path('ciencias_tierra',ciencias_tierra,name='ciencias_tierra'),
    path('cienciasytierra',cienciasytierra,name='cienciasytierra'),
    path('economia_administracion',economia_administracion,name='economia_administracion'),
    path('economiayadministracion',economiayadministracion,name='economiayadministracion'),
    path('sistemas_computacion',sistemas_computacion,name='sistemas_computacion'),
    path('sistemasycomputacion',sistemasycomputacion,name='sistemasycomputacion'),
    path('electrica_electronica',electrica_electronica,name='electrica_electronica'),
    path('electricayelectronica',electricayelectronica,name='electricayelectronica'),
    path('mecanica',mecanica,name='mecanica'),
    path('mecanicaD',mecanicaD,name='mecanicaD'),
    path('industrial',industrial,name='industrial'),
    path('industrialD',industrialD,name='industrialD'),
    path('ciencias_basicas',ciencias_basicas,name='ciencias_basicas'),
    path('ciencia_basica',ciencia_basica,name='ciencia_basica'),
    path('idiomas',idiomas,name='idiomas'),
    path('idioma',idioma,name='idioma'),
]