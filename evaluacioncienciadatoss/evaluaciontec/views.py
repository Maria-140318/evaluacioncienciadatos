from django.shortcuts import render
# Create your views here.
import os
from django.core.management import call_command
from django.conf import settings
from django.shortcuts import render
from subprocess import Popen, PIPE, STDOUT
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.contrib.auth.models import Permission
#from spamanator.utils import get_ip
from django.contrib.auth.decorators import permission_required
#from django.shortcuts import render #, redirect,get_object_or_404,render_to_response
#from django.http import  HttpResponseNotFound #Http404
from django.http import HttpResponse, request
from django.urls import reverse_lazy 
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
import subprocess, gzip
from subprocess import Popen,run
from evaluacioncienciadatoss.settings import DATABASES
from django.core.files.storage import FileSystemStorage
from django.db import transaction
import json
import csv,io
# Importar el módulo pyplot con el alias plt
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import base64
import matplotlib.dates as mdates
from io import BytesIO
from matplotlib.ticker import LinearLocator
#import pandas
#import numpy
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
#import seaborn as sb
#import seaborn as sns
################### 
from .forms import departamentoform, maestrosoform,carreraform
from .forms import  evaluaciondepartamentoform
from .models import departamentos,carrera,maestros,Usuario,evaluaciondepartamento
###################################
##http://127.0.0.1:8000/
##https://vgcode.wordpress.com/2016/11/12/estadisticas-con-django-graphos-y-mongodb/
##http://research.iac.es/sieinvens/python-course/matplotlib.html
#Permisos
def check(request):
        try:
            passwd = DATABASES['default']['PASSWORD']#pasword
            user = DATABASES['default']['USER']#nombre Superuser
            use= request.Get.get("username") #usuario q se esta creando aqui meter nombre caja de text ("ct")
            pasw= request.Get.get("password") #usuario q se esta creando aqui meter el nombre de las cajadetex
            ######## de aqui 
            permisos= request.POST.getlist('perm[]')
            i=len('perm[]')
            if i==0:
                privileges=" "
                command = "mysql -u"+user+"-p"+passwd+"--init-command=\"GRANT "+ privileges +" ON BDD.* TO '"+use+"'@'localhost' IDENTIFIED BY '"+pasw+"'\""
                subprocess.run(command )
            if i==1:
                privileges=" "+permisos[0]
                command = "mysql -u"+user+"-p"+passwd+"--init-command=\"GRANT "+ privileges +" ON BDD.* TO '"+use+"'@'localhost' IDENTIFIED BY '"+pasw+"'\""
                subprocess.run(command )
            if i==2:  
                privileges=" "+permisos[0]+","+permisos[1]
                command = "mysql -u"+user+"-p"+passwd+"--init-command=\"GRANT "+ privileges +" ON BDD.* TO '"+use+"'@'localhost' IDENTIFIED BY '"+pasw+"'\""
                subprocess.run(command )
            if i==3:
                privileges=" "+permisos[0]+","+permisos[1]+","+permisos[2]
                command = "mysql -u"+user+"-p"+passwd+"--init-command=\"GRANT "+ privileges +" ON BDD.* TO '"+use+"'@'localhost' IDENTIFIED BY '"+pasw+"'\""
                subprocess.run(command )
            if i==4:
                privileges=" "+permisos[0]+","+permisos[1]+","+permisos[2]+","+permisos[3]
                command = "mysql -u"+user+"-p"+passwd+"--init-command=\"GRANT "+ privileges +" ON BDD.* TO '"+use+"'@'localhost' IDENTIFIED BY '"+pasw+"'\""
                subprocess.run(command )
        except :
             print()

        return render(request,"evaluaciontec/permisos.html")
def index(request):

    return render(request, 'evaluaciontec/index.html')

###################################################################Respaldo de la BD
def respaldo(request):
    if request.method == 'POST':
        backup_file = request.FILES.get('backup_file')
        if backup_file:
            # Save the backup file to a temporary location
            with open(os.path.join(settings.MEDIA_ROOT, 'backup.sql'), 'wb+') as temp_file:
                for chunk in backup_file.chunks():
                    temp_file.write(chunk)
            # Restore the backup file
            restore_command = f'mysql --user={settings.DATABASES["default"]["USER"]} --password={settings.DATABASES["default"]["PASSWORD"]} {settings.DATABASES["default"]["NAME"]} < {os.path.join(settings.MEDIA_ROOT, "backup.sql")}'
            process = Popen(restore_command, shell=True, stdout=PIPE, stderr=STDOUT)
            output, _ = process.communicate()
            if process.returncode == 0:
                # Delete the temporary backup file
                os.remove(os.path.join(settings.MEDIA_ROOT, 'backup.sql'))
                return render(request, 'evaluaciontec/restaurar.html', {'success': True})
            else:
                return render(request, 'evaluaciontec/restaurar.html', {'error': output.decode()})
        else:
            return render(request, 'evaluaciontec/restaurar.html', {'error': 'No file was uploaded'})
    else:
        return render(request, 'evaluaciontec/restaurar.html')
def backup(request):
    name = DATABASES['default']['NAME']
    passwd = DATABASES['default']['PASSWORD']
    user = DATABASES['default']['USER']
    #mysqldump -u root -p evaluaion > C:/respaldos/agenda1.sql
    proc = subprocess.Popen("C:/xampp/mysql/bin/mysqldump -u "+user+" -p"+passwd+" "+name+" > "+ "C:/respaldos/backup.sql", shell=True)
    procs = subprocess.Popen("tar -czvf "+ "C:/respaldos/backup.tar.tgz "+ "C:/respaldos/backup.sql", shell=True, )
    procs.wait()
    fs = FileSystemStorage("C:/respaldos/")
    with fs.open('backup.tar.tgz') as tar:
        response = HttpResponse(tar, content_type='application/x-gzip')
        response['Content-Disposition'] = 'filename="backup.tar.tgz"'
        return response

############################################################
#def Handler404(request, exception):
#  from django.shortcuts import render
#  return render(request, '404.html')
#def Handler500(request, exception):
#  from django.shortcuts import render
#  return render(request, '500.html')
####################################################################################################
#########################   views de ciencia de datos ############################################## 
####################################################################################################
def get_graph():
    buffer= BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)
    image_png= buffer.getvalue()
    graph=base64.b64encode(image_png)
    graph=graph.decode('utf-8')
    buffer.close()
    return graph
#####
def get_plotc(depa,titulo,nombrex,nombrey):
    qs  =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(nombre='TOTAL:').filter(aspectos='A) Dominio de la Asignatura')
    qs2 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(nombre='TOTAL:').filter(aspectos='B) Planificación del Curso')
    qs3 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(nombre='TOTAL:').filter(aspectos='C) Ambientes de Aprendizaje')
    qs4 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(nombre='TOTAL:').filter(aspectos='D) Estrategias, Métodos y Técnicas')
    qs5 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(nombre='TOTAL:').filter(aspectos='E) Motivación')
    qs6 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(nombre='TOTAL:').filter(aspectos='F) Evaluación')
    qs7 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(nombre='TOTAL:').filter(aspectos='G) Comunicación')
    qs8 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(nombre='TOTAL:').filter(aspectos='H) Gestion del Curso')
    qs9 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(nombre='TOTAL:').filter(aspectos='I) Tecnologías de la Información y Comunicación')
    qs10=evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(nombre='TOTAL:').filter(aspectos='J) Satisfacción General')
    y=[y.puntaje for y in qs]
    y2=[y2.puntaje for y2 in qs2]
    y3=[y3.puntaje for y3 in qs3]
    y4=[y4.puntaje for y4 in qs4]
    y5=[y5.puntaje for y5 in qs5]
    y6=[y6.puntaje for y6 in qs6]
    y7=[y7.puntaje for y7 in qs7]
    y8=[y8.puntaje for y8 in qs8]
    y9=[y9.puntaje for y9 in qs9]
    y10=[y10.puntaje for y10 in qs10]    
    x=[x.semestre for x in qs]  
    plt.subplots()
    plt.switch_backend('AGG')
    plt.figure(figsize=(30,15))
    plt.title(titulo)
    plt.plot(x,y  ,"o",label='A') 
    plt.plot(x,y2 ,"o",label='B') 
    plt.plot(x,y3 ,"o",label="C")
    plt.plot(x,y4 ,"o",label="D") 
    plt.plot(x,y5 ,"o",label="E")
    plt.plot(x,y6 ,"o",label="F")
    plt.plot(x,y7 ,"o",label="G") 
    plt.plot(x,y8 ,"o",label="H") 
    plt.plot(x,y9 ,"o",label="I")
    plt.plot(x,y10,"o",label="J") 
      
    plt.xticks(rotation=45)    
    plt.xlabel(nombrex)
    plt.ylabel(nombrey) 
    plt.legend()      
    fig=get_graph()
    return fig
import matplotlib.pyplot as plt
def get_plot(depa,titulo,nombrex,nombrey):
    qs  =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(nombre='TOTAL:').filter(aspectos='A) Dominio de la Asignatura')
    qs2 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(nombre='TOTAL:').filter(aspectos='B) Planificación del Curso')
    qs3 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(nombre='TOTAL:').filter(aspectos='C) Ambientes de Aprendizaje')
    qs4 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(nombre='TOTAL:').filter(aspectos='D) Estrategias, Métodos y Técnicas')
    qs5 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(nombre='TOTAL:').filter(aspectos='E) Motivación')
    qs6 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(nombre='TOTAL:').filter(aspectos='F) Evaluación')
    qs7 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(nombre='TOTAL:').filter(aspectos='G) Comunicación')
    qs8 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(nombre='TOTAL:').filter(aspectos='H) Gestion del Curso')
    qs9 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(nombre='TOTAL:').filter(aspectos='I) Tecnologías de la Información y Comunicación')
    qs10=evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(nombre='TOTAL:').filter(aspectos='J) Satisfacción General')
    y=[y.puntaje for y in qs]
    y2=[y2.puntaje for y2 in qs2]
    y3=[y3.puntaje for y3 in qs3]
    y4=[y4.puntaje for y4 in qs4]
    y5=[y5.puntaje for y5 in qs5]
    y6=[y6.puntaje for y6 in qs6]
    y7=[y7.puntaje for y7 in qs7]
    y8=[y8.puntaje for y8 in qs8]
    y9=[y9.puntaje for y9 in qs9]
    y10=[y10.puntaje for y10 in qs10]       
    x=[x.year for x in qs2]  
    plt.subplots()
    plt.switch_backend('AGG')
    plt.figure(figsize=(30,15))
    plt.title(titulo)
    plt.plot(x,y  ,"--v",label='A', color='red') 
    plt.plot(x,y2 ,"--o",label='B',color='blue') 
    plt.plot(x,y3 ,"--^",label="C",color='green')
    plt.plot(x,y4 ,"--<",label="D",color='orange') 
    plt.plot(x,y5 ,"-->",label="E",color='indigo')
    plt.plot(x,y6 ,"--.",label="F",color='pink')
    plt.plot(x,y7 ,"--*",label="G",color='grey') 
    plt.plot(x,y8 ,"--+",label="H",color='gold') 
    plt.plot(x,y9 ,"--h",label="I",color='lime')
    plt.plot(x,y10,"--p",label="J",color='cyan')  
    plt.xticks(rotation=45)    
    plt.xlabel(nombrex)
    plt.ylabel(nombrey) 
    plt.legend()      
    fig=get_graph()
    return fig
def get_plots(depa,titulo,nombrex,nombrey,nombre):
    qs  =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos='A) Dominio de la Asignatura').filter(nombre=nombre)
    qs2 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos='B) Planificación del Curso').filter(nombre=nombre)
    qs3 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos='C) Ambientes de Aprendizaje').filter(nombre=nombre)
    qs4 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos='D) Estrategias, Métodos y Técnicas').filter(nombre=nombre)
    qs5 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos='E) Motivación').filter(nombre=nombre)
    qs6 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos='F) Evaluación').filter(nombre=nombre)
    qs7 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos='G) Comunicación').filter(nombre=nombre)
    qs8 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos='H) Gestion del Curso').filter(nombre=nombre)
    qs9 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos='I) Tecnologías de la Información y Comunicación').filter(nombre=nombre)
    qs10=evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos='J) Satisfacción General').filter(nombre=nombre)
    y=[y.puntaje for y in qs]
    y2=[y2.puntaje for y2 in qs2]
    y3=[y3.puntaje for y3 in qs3]
    y4=[y4.puntaje for y4 in qs4]
    y5=[y5.puntaje for y5 in qs5]
    y6=[y6.puntaje for y6 in qs6]
    y7=[y7.puntaje for y7 in qs7]
    y8=[y8.puntaje for y8 in qs8]
    y9=[y9.puntaje for y9 in qs9]
    y10=[y10.puntaje for y10 in qs10]    
    x=[x.year for x in qs2]   
    plt.switch_backend('AGG')
    plt.figure(figsize=(30,15))
    plt.title(titulo)
    #plt.subplot(2,5,1)
    plt.plot(x,y,"--o",label='A',color='blue')  
    #plt.subplot(2,5,2)           
    plt.plot(x,y2,"--o",label='B',color='green') 
    #plt.subplot(2,5,3) 
    plt.plot(x,y3,"--o",label="C",color='red')
    #plt.subplot(2,5,4)
    plt.plot(x,y4,"--o",label="D",color='pink') 
    #plt.subplot(2,5,5)      
    plt.plot(x,y5,"--o",label="E",color='orange') 
    #plt.subplot(2,5,6)       
    plt.plot(x,y6,"--o",label="F",color='gold')
    #plt.subplot(2,5,7)
    plt.plot(x,y7,"--o",label="G",color='indigo')
    #plt.subplot(2,5,8)   
    plt.plot(x,y8,"--o",label="H",color='crimson') 
    #plt.subplot(2,5,9)
    plt.plot(x,y9,"--o",label="I",color='grey') 
    #plt.subplot(2,5,10)    
    plt.plot(x,y10,"--o",label="J",color='lime') 
    plt.xticks(rotation=45)    
    plt.xlabel(nombrex)
    plt.ylabel(nombrey) 
    plt.legend()    
    plt.show()
    fig=get_graph()
    return fig
def get_plotx(depa,titulo,nombrex,nombrey,inciso):
    qs  =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos=inciso).filter(nombre='TOTAL:')
    qss =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos=inciso).filter(nombre='TOTAL:')
    
    y=[y.puntaje for y in qs]
    y1=[y.puntaje for y in qss]
    x=[x.year for x in qs]
    #plt.subplots()
    plt.switch_backend('AGG')
    plt.figure(figsize=(14,9))
    plt.title(titulo)
    plt.plot(x,y  ,'--o',linewidth=4, color='blue', label="A") 
    
    plt.xticks(rotation=45)    
    plt.xlabel(nombrex)
    plt.ylabel(nombrey) 
    plt.legend()    
    fig=get_graph()
    return fig
def get_plotsx(depa,titulo,nombrex,nombrey,aspecto,nombre):
    qs  =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos=aspecto).filter(nombre=nombre).exclude(nombre='TOTAL:')
    y=[y.puntaje for y in qs]
    x=[x.year for x in qs]
    plt.subplots()
    plt.switch_backend('AGG')
    plt.figure(figsize=(30,15))
    plt.title(titulo)
    plt.plot(x,y,"--o")    
    plt.xticks(rotation=45)    
    plt.xlabel(nombrex)
    plt.ylabel(nombrey) 
    plt.legend()    
    fig=get_graph()
    return fig
def get_plotss(depa,titulo,nombrex,nombrey):
    qs  =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos='A) Dominio de la Asignatura').exclude(nombre='TOTAL:')
    qs2 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos='B) Planificación del Curso').exclude(nombre='TOTAL:')
    qs3 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos='C) Ambientes de Aprendizaje').exclude(nombre='TOTAL:')
    qs4 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos='D) Estrategias, Métodos y Técnicas').exclude(nombre='TOTAL:')
    qs5 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos='E) Motivación').exclude(nombre='TOTAL:')
    qs6 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos='F) Evaluación').exclude(nombre='TOTAL:')
    qs7 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos='G) Comunicación').exclude(nombre='TOTAL:')
    qs8 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos='H) Gestion del Curso').exclude(nombre='TOTAL:')
    qs9 =evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos='I) Tecnologías de la Información y Comunicación').exclude(nombre='TOTAL:')
    qs10=evaluaciondepartamento.objects.filter(idDepartamento=depa).filter(aspectos='J) Satisfacción General').exclude(nombre='TOTAL:')
    y=[y.puntaje for y in qs]
    y2=[y2.puntaje for y2 in qs2]
    y3=[y3.puntaje for y3 in qs3]
    y4=[y4.puntaje for y4 in qs4]
    y5=[y5.puntaje for y5 in qs5]
    y6=[y6.puntaje for y6 in qs6]
    y7=[y7.puntaje for y7 in qs7]
    y8=[y8.puntaje for y8 in qs8]
    y9=[y9.puntaje for y9 in qs9]
    y10=[y10.puntaje for y10 in qs10]    
    x=[x.nombre for x in qs2]   
    plt.switch_backend('AGG')
    plt.figure(figsize=(30,15))
    plt.title(titulo)
    #plt.subplot(2,5,1)
    plt.plot(x,y,"--o",label='A',color='blue')  
    #plt.subplot(2,5,2)           
    plt.plot(x,y2,"--o",label='B',color='green') 
    #plt.subplot(2,5,3) 
    plt.plot(x,y3,"--o",label="C",color='red')
    #plt.subplot(2,5,4)
    plt.plot(x,y4,"--o",label="D",color='red') 
    #plt.subplot(2,5,5)      
    plt.plot(x,y5,"--o",label="E",color='orange') 
    #plt.subplot(2,5,6)       
    plt.plot(x,y6,"--o",label="F",color='gold')
    #plt.subplot(2,5,7)
    plt.plot(x,y7,"--o",label="G",color='indigo')
    #plt.subplot(2,5,8)   
    plt.plot(x,y8,"--o",label="H",color='crimson') 
    #plt.subplot(2,5,9)
    plt.plot(x,y9,"--o",label="I",color='grey') 
    #plt.subplot(2,5,10)    
    plt.plot(x,y10,"--o",label="J",color='lime') 
    plt.xticks(rotation=45)    
    plt.xlabel(nombrex)
    plt.ylabel(nombrey) 
    plt.legend()    
    plt.show()
    fig=get_graph()
    return fig
################################### ciencias de la tierra
from .forms import opcionform,depaUnoform,depaDosform,depaTresform,depaCuatroform, depaCincoform,depaSeisform,depaSieteform,depaOchoform
from tkinter import ttk
from tkinter import *
def ciencias_tierra(request):
    form=opcionform() 
    if request.method == 'POST':       
       select = request.POST.get('Aspectos')
       if(select=='K) Todos'):
            chart=get_plot('1','Ciencias de la Tierrra','Año','Puntaje')
            filtro=evaluaciondepartamento.objects.filter(idDepartamento='1').filter(nombre='TOTAL:').exclude(aspectos='Aspectos Evaluados')
       else:
            chart=get_plotx('1',select,'Año','Puntaje',select)
            filtro=evaluaciondepartamento.objects.filter(idDepartamento='1').filter(nombre='TOTAL:').filter(aspectos=select).exclude(aspectos='Aspectos Evaluados')
       
    else:         
           chart=get_plot('1','Ciencias de la Tierra','Año','Puntaje')  
           filtro=evaluaciondepartamento.objects.filter(idDepartamento='1').filter(nombre='TOTAL:').exclude(aspectos='Aspectos Evaluados')
       
    return render(request,'evaluaciontec/ciencias_tierra.html',{'form': form ,'chart':chart,'filtro':filtro})

def cienciasytierra(request): 
    form=depaUnoform()     
    formd=opcionform()     
    if request.method == 'POST':       
       select = request.POST.get('Aspectos')
       selectd=request.POST.get('maestros') 
       if(select=='K) Todos' and selectd!=''):
            chart=get_plots('1','Ciencias y Tierra','Año','Puntaje',selectd)
       if(select=='' or selectd==''):
           chart=get_plotss('1','Ciencias de la Tierra','Maestros','Puntaje')
       else:
           chart=get_plotsx('1',select+" "+selectd,'Año','Puntaje',select,selectd)
    else:  
     chart=get_plotss('1','Ciencias de la Tierra','Maestros','Puntaje')
    return render(request,'evaluaciontec/cienciasytierra.html',{'form':form,'formd':formd,'chart':chart})
######################################################## economia y administracion
def economia_administracion(request):
    form=opcionform()   
    if request.method == 'POST':       
       select = request.POST.get('Aspectos')
       
       if(select=='K) Todos'):
                  chart=get_plot('2','Economía y Administración','Año','Puntaje')
                  filtro=evaluaciondepartamento.objects.filter(idDepartamento='2').filter(nombre='TOTAL:').exclude(aspectos='Aspectos Evaluados')
       
       else:
             chart=get_plotx('2',select,'Año','Puntaje',select)
             filtro=evaluaciondepartamento.objects.filter(idDepartamento='2').filter(nombre='TOTAL:').filter(aspectos=select).exclude(aspectos='Aspectos Evaluados')
    else:         
        chart=get_plot('2','Economía y Administración','Año','Puntaje') 
        filtro=evaluaciondepartamento.objects.filter(idDepartamento='2').filter(nombre='TOTAL:').exclude(aspectos='Aspectos Evaluados')
               
    return render(request,'evaluaciontec/economia_administracion.html',{'form': form ,'chart':chart,'filtro':filtro})
def economiayadministracion(request):   
    form=depaDosform()     
    formd=opcionform()     
    if request.method == 'POST':       
       select = request.POST.get('Aspectos')
       selectd=request.POST.get('maestros') 
       if(select=='K) Todos'):
            chart=get_plots('2','Economía y Administración','Semestre','Puntaje',selectd)
       if(select=='' or selectd==''):
           chart=get_plotss('2','Economía y Administración','Maestros','Puntaje')
       else:
           chart=get_plotsx('2',select+" "+selectd,'Semestre','Puntaje',select,selectd)
    else:  
     chart=get_plotss('2','Economía y Administración','Maestros','Puntaje') 
    return render(request,'evaluaciontec/economiayadministracion.html',{'form':form,'formd':formd,'chart':chart})
#####################Sistemas y computación
def sistemas_computacion(request): 
    form=opcionform()   
    if request.method == 'POST':       
       select = request.POST.get('Aspectos')
       if(select=='K) Todos'):
                  chart=get_plot('3','Sistemas y Computación','Año','Puntaje')
                  filtro=evaluaciondepartamento.objects.filter(idDepartamento='3').filter(nombre='TOTAL:').exclude(aspectos='Aspectos Evaluados')
        
       else:
             chart=get_plotx('3',select,'Semestre','Año',select) 
             filtro=evaluaciondepartamento.objects.filter(idDepartamento='3').filter(nombre='TOTAL:').filter(aspectos=select).exclude(aspectos='Aspectos Evaluados')   
    else:         
        chart=get_plot('3','Sistemas y Computacion','Año','puntaje')   
        filtro=evaluaciondepartamento.objects.filter(idDepartamento='3').filter(nombre='TOTAL:').exclude(aspectos='Aspectos Evaluados')
        
    return render(request,'evaluaciontec/sistemas_computacion.html',{'form': form ,'chart':chart,'filtro':filtro})

def sistemasycomputacion(request): 
    form=depaTresform()     
    formd=opcionform()     
    if request.method == 'POST':       
       select = request.POST.get('Aspectos')
       selectd=request.POST.get('maestros') 
       if(select=='K) Todos' and selectd!=''):
            chart=get_plots('3','Sistemas y Computación','Semestre','Puntaje',selectd)
       if(select=='' or selectd==''):
           chart=get_plotss('3','Sistemas y Computación','Maestros','Puntaje')
       else:
           chart=get_plotsx('3',select+" "+selectd,'Semestre','Puntaje',select,selectd)
    else:  
     chart=get_plotss('3','Sistemas y Computación','Maestros','Puntaje')    
    return render(request,'evaluaciontec/sistemasycomputacion.html',{'form': form ,'formd':formd,'chart':chart})

################################
def electrica_electronica(request):
    form=opcionform()   
    if request.method == 'POST':       
       select = request.POST.get('Aspectos')
       if(select=='K) Todos'):
            chart=get_plot('4','Electrica y Electrónica','Año','Puntaje') 
            filtro=evaluaciondepartamento.objects.filter(idDepartamento='4').filter(nombre='TOTAL:').exclude(aspectos='Aspectos Evaluados')
           
       else:
            chart=get_plotx('4',select,'Año','Puntaje',select) 
            filtro=evaluaciondepartamento.objects.filter(idDepartamento='4').filter(nombre='TOTAL:').filter(aspectos=select).exclude(aspectos='Aspectos Evaluados')    
    else:         
        chart=get_plot('4','Electrica y Electronica','Año','Puntaje')
        filtro=evaluaciondepartamento.objects.filter(idDepartamento='4').filter(nombre='TOTAL:').exclude(aspectos='Aspectos Evaluados')
                 
    return render(request,'evaluaciontec/electrica_electronica.html',{'form': form ,'chart':chart,'filtro':filtro})
def electricayelectronica(request):    
    form=depaCuatroform()     
    formd=opcionform()     
    if request.method == 'POST':       
       select = request.POST.get('Aspectos')
       selectd=request.POST.get('maestros') 
       if(select=='K) Todos' and selectd!=''):
            chart=get_plots('4','Electtrica y Electronica','Semestre','Puntaje',selectd)
       if(select=='' or selectd==''):
           chart=get_plotss('4','Electrica y Electronica','Maestros','Puntaje')
       else:
           chart=get_plotsx('4',select+" "+selectd,'Semestre','Puntaje',select,selectd)
    else:  
     chart=get_plotss('4','Electtrica y Electronica','Maestros','Puntaje')  
    return render(request,'evaluaciontec/electricayelectronica.html',{'form': form,'formd':formd,'chart':chart})
##############################
def mecanica(request):  
    form=opcionform()   
    if request.method == 'POST':       
       select = request.POST.get('Aspectos') 
       if(select=='K) Todos'):
            chart=get_plot('5','Mecanica','Año','Puntaje') 
            filtro=evaluaciondepartamento.objects.filter(idDepartamento='5').filter(nombre='TOTAL:').exclude(aspectos='Aspectos Evaluados')
           
       else:
            chart=get_plotx('5',select,'Año','Puntaje',select) 
            filtro=evaluaciondepartamento.objects.filter(idDepartamento='5').filter(nombre='TOTAL:').filter(aspectos=select).exclude(aspectos='Aspectos Evaluados')   
    else:
     chart=get_plot('5','Mecanica','Año','Puntaje')
     filtro=evaluaciondepartamento.objects.filter(idDepartamento='5').filter(nombre='TOTAL:').exclude(aspectos='Aspectos Evaluados')
         
    return render(request,'evaluaciontec/mecanica.html',{'form': form,'chart':chart,'filtro':filtro})

def mecanicaD(request): 
    form=depaCincoform()     
    formd=opcionform()     
    if request.method == 'POST':       
       select = request.POST.get('Aspectos')
       selectd=request.POST.get('maestros') 
       if(select=='K) Todos' and selectd!=''):
            chart=get_plots('5','Mecanica','Semestre','Puntaje',selectd)
       if(select=='' or selectd==''):
           chart=get_plotss('5','Mecanica','Maestros','Puntaje')
       else:
           chart=get_plotsx('5',select+" "+selectd,'Semestre','Puntaje',select,selectd)
    else:  
     chart=get_plotss('5','Mecanica','Maestros','Puntaje')     
    return render(request,'evaluaciontec/mecanicaD.html',{'form': form,'formd':formd,'chart':chart})
################################
def industrial(request):
    form=opcionform()   
    if request.method == 'POST':       
       select = request.POST.get('Aspectos')
       if(select=='K) Todos'):
            chart=get_plot('6','Industrial','Año','Puntaje') 
            filtro=evaluaciondepartamento.objects.filter(idDepartamento='6').filter(nombre='TOTAL:').exclude(aspectos='Aspectos Evaluados')
           
       else:
            chart=get_plotx('6',select,'Año','Puntaje',select)
            filtro=evaluaciondepartamento.objects.filter(idDepartamento='6').filter(nombre='TOTAL:').filter(aspectos=select).exclude(aspectos='Aspectos Evaluados')    
    else:    
     chart=get_plot('6','Industrial','Año','Puntaje') 
     filtro=evaluaciondepartamento.objects.filter(idDepartamento='6').filter(nombre='TOTAL:').exclude(aspectos='Aspectos Evaluados')
        
    return render(request,'evaluaciontec/industrial.html',{'form':form,'chart':chart,'filtro':filtro})
def industrialD(request):  
    form=depaSeisform()     
    formd=opcionform()     
    if request.method == 'POST':       
       select = request.POST.get('Aspectos')
       selectd=request.POST.get('maestros') 
       if(select=='K) Todos' and selectd!=''):
            chart=get_plots('6','Industrial','Semestre','Puntaje',selectd)
       if(select=='' or selectd==''):
           chart=get_plotss('6','Industrial','Maestros','Puntaje')
       else:
           chart=get_plotsx('6',select+" "+selectd,'Semestre','Puntaje',select,selectd)
    else:  
     chart=get_plotss('6','Industrial','Maestros','Puntaje')        
    return render(request,'evaluaciontec/industrialD.html',{'form': form,'formd':formd,'chart':chart})
#####################################
def ciencias_basicas(request):
    form=opcionform()   
    if request.method == 'POST':       
       select = request.POST.get('Aspectos')
       if(select=='K) Todos'):
            chart=get_plot('7','Ciencias Basicas','Año','Puntaje') 
            filtro=evaluaciondepartamento.objects.filter(idDepartamento='7').filter(nombre='TOTAL:').exclude(aspectos='Aspectos Evaluados')
        
       else:
            chart=get_plotx('7',select,'Año','Puntaje',select)
            filtro=evaluaciondepartamento.objects.filter(idDepartamento='7').filter(nombre='TOTAL:').filter(aspectos=select).exclude(aspectos='Aspectos Evaluados')    
    else:    
     chart=get_plot('7','Ciencias Basicas','Año','Puntaje')
    filtro=evaluaciondepartamento.objects.filter(idDepartamento='7').filter(nombre='TOTAL:').exclude(aspectos='Aspectos Evaluados')
      
    return render(request,'evaluaciontec/ciencias_basicas.html',{'form':form,'chart':chart,'filtro':filtro})

def ciencia_basica(request):  
    form=depaSieteform()     
    formd=opcionform()     
    if request.method == 'POST':       
       select = request.POST.get('Aspectos')
       selectd=request.POST.get('maestros') 
       if(select=='K) Todos' and selectd!=''):
            chart=get_plots('7','Ciencias Basicas','Semestre','Puntaje',selectd)
       if(select=='' or selectd==''):
           chart=get_plotss('7','Ciencias Basicas','Maestros','Puntaje')
       else:
           chart=get_plotsx('7',select+" "+selectd,'Semestre','Puntaje',select,selectd)
    else:  
     chart=get_plotss('7','Ciencias Basicas','Maestros','Puntaje')     
    return render(request,'evaluaciontec/ciencia_basica.html',{'form': form,'formd':formd,'chart':chart})
######################################
def idiomas(request):
    form=opcionform()   
    if request.method == 'POST':       
       select = request.POST.get('Aspectos')
       if(select=='K) Todos'):
            chart=get_plot('8','Idiomas','Año','Puntaje')    
            filtro=evaluaciondepartamento.objects.filter(idDepartamento='8').filter(nombre='TOTAL:').exclude(aspectos='Aspectos Evaluados')
     
       else:
            chart=get_plotx('8',select,'Año','Puntaje',select)                  
    else:
     chart=get_plot('8','Idiomas','Año','Puntaje') 
     filtro=evaluaciondepartamento.objects.filter(idDepartamento='8').filter(nombre='TOTAL:').exclude(aspectos='Aspectos Evaluados')
     
    return render(request,'evaluaciontec/idiomas.html',{'form':form,'chart':chart,'filtro':filtro})
def idioma(request):
    form=depaOchoform()     
    formd=opcionform()     
    if request.method == 'POST':       
       select = request.POST.get('Aspectos')
       selectd=request.POST.get('maestros') 
       if(select=='K) Todos' and selectd!=''):
            chart=get_plots('8','Idiomas','Semestre','Puntaje',selectd)
       if(select=='' or selectd==''):
           chart=get_plotss('8','Idiomas','Maestros','Puntaje')
       else:
           chart=get_plotsx('8',select+" "+selectd,'Semestre','Puntaje',select,selectd)
    else:  
     chart=get_plotss('8','Idiomas','Maestros','Puntaje')
    return render(request,'evaluaciontec/idioma.html',{'form': form,'formd':formd,'chart':chart})

########################################################################################################################
###########################             Views   CRUD                #########################################################


@permission_required('admin.can_add_log_entry')
def departamentos_download(request):
    items=departamentos.objects.all()    
    response=HttpResponse(content_type='text/csv')    
    response['Content-Disposition']='attachment; filename="departamento.csv"'   
    writer =csv.writer(response,delimiter=',')
    writer.writerow(['idDepartamento','nombre'])
    for obj in items:
        writer.writerow([obj.idDepartamento,obj.nombre])
    return response

@permission_required('admin.can_add_log_entry')
def departamento_upload(request):
    template="evaluaciontec/upload.html"
    prompt = {
        'order':'El orden del CSV debe ser Id,nombre'
    }

    if request.method=="GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request,'No es un archivo csv')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
         _, created = departamentos.objects.update_or_create(
        idDepartamento=column[0],
        nombre=column[1]
                )
    context={}
    return render(request, template, context)
####
class DepartamentoList(ListView):
    model = departamentos
    template_name = 'evaluaciontec/consultar_departamento.html'

class DepartamentoCreate(CreateView):
    model = departamentos
    form_class = departamentoform
    template_name = 'evaluaciontec/añadir_departamento.html'
    success_url = reverse_lazy('ver_departamento')

class DepartamentoUpdate(UpdateView):
    model =  departamentos
    form_class = departamentoform
    template_name = 'evaluaciontec/añadir_departamento.html'
    success_url = reverse_lazy('ver_departamento')

class DepartamentoDelete(DeleteView):
    model = departamentos
    form_class = departamentoform
    template_name = 'evaluaciontec/eliminar.html'
    success_url = reverse_lazy('ver_departamento')
##############################################################################carrera
################################################################################################
@permission_required('admin.can_add_log_entry')
def carrera_download(request):
    items=carrera.objects.all()
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename="carrera.csv"'
    writer =csv.writer(response,delimiter=',')
    writer.writerow(['idCarrera','nombre','idDepartamento'])
    for obj in items:
        writer.writerow([obj.idCarrera, obj.nombre,obj.idDepartamento])
    return response

@permission_required('admin.can_add_log_entry')
def carrera_upload(request):
    template="evaluaciontec/upload.html"

    prompt = {
        'order':'El orden del CSV debe ser idCarrera, nombre, idDepartamento'
    }

    if request.method=="GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request,'No es un archivo csv')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
         _, created = carrera.objects.update_or_create(
        idCarrera=column[0],
        nombre=column[1],
        idDepartamento=column[2]
                )
    context={}
    return render(request, template, context)
class CarreraList(ListView):
    model = carrera
    template_name = 'evaluaciontec/consultar_carrera.html'
    context_object_name = 'object_list'

class CarreraCreate(CreateView):
    model = carrera
    form_class = carreraform
    template_name = 'evaluaciontec/añadir_carrera.html'
    success_url = reverse_lazy('ver_carrera')

class CarreraUpdate(UpdateView):
    model =  carrera
    form_class = carreraform
    template_name = 'evaluaciontec/añadir_carrera.html'
    success_url = reverse_lazy('ver_carrera')

class CarreraDelete(DeleteView):
    model = carrera
    form_class = carreraform
    template_name = 'evaluaciontec/eliminar.html'
    success_url = reverse_lazy('ver_carrera')

################################Maestros####################################
###############################################
@permission_required('admin.can_add_log_entry')
def maestros_download(request):
    items=maestros.objects.all()
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename="maestros.csv"'
    writer =csv.writer(response,delimiter=',')
    writer.writerow(['idMaestro','plantel','idDepartamento','rfc','curp','apellidoPaterno','apellidoMaterno','nombre','email'])
    for obj in items:
        writer.writerow([obj.idMaestro,obj.plantel,obj.idDepartamento,obj.rfc,obj.curp,obj.apellidoPaterno,obj.apellidoMaterno,obj.nombre,obj.email])
    return response 

@permission_required('admin.can_add_log_entry')
def maestros_upload(request):
    template="evaluaciontec/upload.html"

    prompt = {
        'order':'El orden del CSV debe ser idMaestro,plantel,idDepartamento,rfc,curp,apellidoPaterno,apellidoMaterno,nombre,email'
    }

    if request.method=="GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request,'No es un archivo csv')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
         _, created = Usuario.objects.update_or_create(
        idMaestro= column[0],
        plantel= column[1],
        idDepartamento= column[2],
        rfc= column[3],
        curp= column[4],
        apellidoPaterno= column[5],
        apellidoMaterno= column[6],
        nombre= column[7],
        email= column[8]
                )
    context={}
    return render(request, template, context)

class MaestrosList(ListView):
    model = maestros
    template_name = 'evaluaciontec/consultar_maestro.html'

class MaestrosCreate(CreateView):
    model = maestros
    form_class = maestrosoform
    template_name = 'evaluaciontec/añadir_maestros.html'
    success_url = reverse_lazy('ver_maestros')

class MaestrosUpdate(UpdateView):
    model = maestros
    form_class = maestrosoform
    template_name = 'evaluaciontec/añadir_maestros.html'
    success_url = reverse_lazy('ver_maestros')

class MaestrosDelete(DeleteView):
    model = maestros
    form_class = maestrosoform
    template_name = 'evaluaciontec/eliminar.html'
    success_url = reverse_lazy('ver_maestros')

##########################################################################################
##############################################################################
###########
@permission_required('admin.can_add_log_entry')
def evaluadepa_download(request):
    items=evaluaciondepartamento.objects.all()
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename="evaluadepa.csv"'
    writer =csv.writer(response,delimiter=',')
    writer.writerow(['idEvaluacion','nombre','promedio','numeroAlumnos','aspectos','puntaje','calificacion','year','semestre','idDepartamento'])
    for obj in items:
        writer.writerow([obj.idEvaluacion,obj.nombre,obj.promedio,obj.numeroAlumnos,obj.aspectos,obj.puntaje,obj.calificacion,obj.year,obj.semestre,obj.idDepartamento])
    return response

@permission_required('admin.can_add_log_entry')
def evaluadepa_upload(request):
    template="evaluaciontec/upload.html"

    prompt = {
        'order':'El orden del CSV debe ser idEvaluacion, nombre,promedio, numeroAlumnos, aspectos, puntaje, calificacion,year,semestre,idDepartamento'
    }

    if request.method=="GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request,'No es un archivo csv')

    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
         _, created = carrera.objects.update_or_create(
        idEvaluacion=column[0],
        nombre=column[1],
        promedio=column[2],
        numeroAlumnos= column[3],
        aspectos= column[4],
        puntaje= column[5],
        calificacion=column[6],
        year=column[7],
        semestre=column[8],
        idDepartamento= column[9]
                )
    context={}
    return render(request, template, context)

class EvaluaDepartamentoList(ListView):
    model = evaluaciondepartamento
    template_name = 'evaluaciontec/consultar_evaluadepartamento.html'
class EvaluaDepartamentoCreate(CreateView):
    model = evaluaciondepartamento
    form_class = evaluaciondepartamentoform
    template_name = 'evaluaciontec/añadir_evaluadepartamento.html'
    success_url = reverse_lazy('ver_carrera')
class EvaluaDepartamentoUpdate(UpdateView):
    model =  evaluaciondepartamento
    form_class = evaluaciondepartamentoform
    template_name = 'evaluaciontec/añadir_evaluadepartamento.html'
    success_url = reverse_lazy('ver_carrera')
class EvaluaDepartamentoDelete(DeleteView):
    model = evaluaciondepartamento
    form_class = evaluaciondepartamentoform
    template_name = 'evaluaciontec/eliminar_evaluadepartamento.html'
    success_url = reverse_lazy('ver_departamento')
########################################################################################################
####################################################################################33
################################
#codigo para usuarios django

from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

class UserList(ListView):
    model =User
    template_name = 'evaluaciontec/consultar_usuario.html'
class usuarioList(ListView):
    model =User
    template_name = 'evaluaciontec/consultar_usuario.html'
class UserCreate(CreateView):
    model =User
    form_class = UserRegistrationForm
    template_name = 'evaluaciontec/añadir_usuario.html'
    success_url = reverse_lazy('ver_usuario')
class UserUpdate(UpdateView):
    model =  User
    form_class = UserRegistrationForm
    template_name = 'evaluaciontec/modificar_usuario.html'
    success_url = reverse_lazy('ver_usuario')
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Replace 'home' with the URL name of your home page
    else:
        form = UserRegistrationForm()
    return render(request, 'evaluaciontec/añadir_usuario.html', {'form': form})
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')  # Replace 'profile' with the URL name of the user profile page
    else:
        form = UserRegistrationForm(instance=request.user)
    return render(request, 'evaluaciontec/modificar_usuario.html', {'form': form})