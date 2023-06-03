from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import departamentos, maestros, carrera, evaluaciondepartamento,Usuario

class opcionform(forms.Form):
    SELECT_CHOICES =[
    ('A) Dominio de la Asignatura','A Dominio de la Asignatura'),
    ('B) Planificación del Curso','B Planificación del Curso'),
    ('C) Ambientes de Aprendizaje','C Ambientes de Aprendizaje'),
    ('D) Estrategias, Métodos y Técnicas','D Estrategias, Métodos y Técnicas'),
    ('E) Motivación','E Motivación'),
    ('F) Evaluación','F Evaluación'),
    ('G) Comunicación','G Comunicación'),
    ('H) Gestion del Curso','H Gestion del Curso'),
    ('I) Tecnologías de la Información y Comunicación','I Tecnologías de la Información y Comunicación'),
    ('J) Satisfacción General','J Satisfacción General'),
    ('K) Todos', 'K Todos'),
    ]
    Aspectos = forms.ChoiceField(choices=SELECT_CHOICES)
class depaUnoform(forms.Form):
    e = evaluaciondepartamento.objects.values_list('nombre', flat=True).distinct().filter(idDepartamento='1').exclude(nombre='TOTAL:')
    SELECT_CHOICES = [(lista, lista) for lista in e]
    maestros = forms.ChoiceField(choices=SELECT_CHOICES)
class depaDosform(forms.Form):
    e = evaluaciondepartamento.objects.values_list('nombre', flat=True).distinct().filter(idDepartamento='2').exclude(nombre='TOTAL:')
    SELECT_CHOICES = [(lista, lista) for lista in e]
    maestros = forms.ChoiceField(choices=SELECT_CHOICES)
class depaTresform(forms.Form):
    e = evaluaciondepartamento.objects.values_list('nombre', flat=True).distinct().filter(idDepartamento='3').exclude(nombre='TOTAL:')
    SELECT_CHOICES = [(lista, lista) for lista in e]
    maestros = forms.ChoiceField(choices=SELECT_CHOICES)
class depaCuatroform(forms.Form):
    e = evaluaciondepartamento.objects.values_list('nombre', flat=True).distinct().filter(idDepartamento='4').exclude(nombre='TOTAL:')
    SELECT_CHOICES = [(lista, lista) for lista in e]
    maestros = forms.ChoiceField(choices=SELECT_CHOICES)
class depaCincoform(forms.Form):
    e = evaluaciondepartamento.objects.values_list('nombre', flat=True).distinct().filter(idDepartamento='5').exclude(nombre='TOTAL:')
    SELECT_CHOICES = [(lista, lista) for lista in e]
    maestros = forms.ChoiceField(choices=SELECT_CHOICES)
class depaSeisform(forms.Form):
    e = evaluaciondepartamento.objects.values_list('nombre', flat=True).distinct().filter(idDepartamento='6').exclude(nombre='TOTAL:')
    SELECT_CHOICES = [(lista, lista) for lista in e]
    maestros = forms.ChoiceField(choices=SELECT_CHOICES)
class depaSieteform(forms.Form):
    e = evaluaciondepartamento.objects.values_list('nombre', flat=True).distinct().filter(idDepartamento='7').exclude(nombre='TOTAL:')
    SELECT_CHOICES = [(lista, lista) for lista in e]
    maestros = forms.ChoiceField(choices=SELECT_CHOICES)
class depaOchoform(forms.Form):
    e = evaluaciondepartamento.objects.values_list('nombre', flat=True).distinct().filter(idDepartamento='8').exclude(nombre='TOTAL:')
    SELECT_CHOICES = [(lista, lista) for lista in e]
    maestros = forms.ChoiceField(choices=SELECT_CHOICES)

    
class departamentoform(forms.ModelForm):
    class Meta:
        model = departamentos
        fields = [
            'idDepartamento',
            'nombre',
        ]
        labels = {
            'idDepartamento' : 'identificador del departamento',
            'nombre' : 'nombre departamento',
        }
        widgets = {
            'idDepartamento' : forms.TextInput(attrs={'class':'form-control'}),
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),            
        }
class maestrosoform(forms.ModelForm):
    class Meta:
        model = maestros
        fields = [
            'idMaestro',
            'plantel',
            'idDepartamento',
            'rfc',
            'curp',
            'apellidoPaterno',
            'apellidoMaterno',
            'nombre',
            'email',
        ]
        labels = {
            'idMaestro' : 'idMaestro',
            'plantel' : 'plantel',
            'idDepartamento' : 'identificador del departamento',
            'rfc' : 'rfc' ,
            'curp' : 'curp',
            'apellidoPaterno' : 'apellido Paterno',
            'apellidoMaterno' : 'apellido Materno',
            'nombre' : 'nombre',
            'email' : 'email',
            
        }
        widgets = {
            'idMaestro' : forms.TextInput(attrs={'class':'form-control'}),             
            'plantel' : forms.TextInput(attrs={'class':'form-control'}),
            'idDepartamento' : forms.TextInput(attrs={'class':'form-control'}),
            'rfc' : forms.TextInput(attrs={'class':'form-control'}),
            'curp' :forms.TextInput(attrs={'class':'form-control'}),
            'apellidoPaterno' : forms.TextInput(attrs={'class':'form-control'}),
            'apellidoMaterno' : forms.TextInput(attrs={'class':'form-control'}),
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.TextInput(attrs={'class':'form-control'}),            
        }
class carreraform(forms.ModelForm):
    class Meta:
        model = carrera
        fields = [
            'idCarrera',
            'nombre',
            'idDepartamento',
        ]
        labels = {
            'idCarrera' : 'idCarrera',
            'nombre' : 'nombre',
            'idDepartamento' : 'identificador del departamento',
        }
        widgets = {
            'idCarrera' : forms.TextInput(attrs={'class':'form-control'}),
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'idDepartamento' : forms.TextInput(attrs={'class':'form-control'}),            
        }

class evaluaciondepartamentoform(forms.ModelForm):
    class Meta:
        model =evaluaciondepartamento
        fields = [
            'idEvaluacion',
            'nombre',
            'promedio',
            'numeroAlumnos',
            'aspectos',            
            'puntaje',
            'calificacion',
            'idDepartamento',
            'year',            
            'semestre',
            
        ]
        labels = {
            'idEevaluacion': 'identificador',
            'nombre': 'nombre',
            'promedio':'promedio',
            'numeroAlumnos':'numero alumnos',
            'aspectos':'aspectos',         
            'puntaje': 'puntaje',
            'calificacion': 'calificacion',  
            'semestre': 'semestre',
            'idDepartamento' :'identificador del departamento' ,
            'year':'año',        
            
        }
        widgets = {
            'idEvaluacion': forms.TextInput(attrs={'class':'form-control'}),
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'promedio':forms.NumberInput(attrs={'class':'form-control'}),
            'numeroAlumnos': forms.NumberInput(attrs={'class':'form-control'}),
            'aspectos': forms.TextInput(attrs={'class':'form-control'}),         
            'puntaje':forms.TextInput(attrs={'class':'form-control'}),
            'calificacion':forms.TextInput(attrs={'class':'form-control'}), 
            'idDepartamento' : forms.TextInput(attrs={'class':'form-control'}),            
            'year':forms.TextInput(attrs={'class':'form-control'}),      
            'semestre':forms.TextInput(attrs={'class':'form-control'}),
           
        }  

        
class Usuarioform(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'idU',
            'email',
            'nombres',
            'apellidos',
        ]
        labels = {
            'idU' : 'identificador',
            'email' : 'email',
            'nombres' : 'nombre(s)',
            'apellidos' : 'apellido(s)',
        }
        widgets = {
            'idU' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.TextInput(attrs={'class':'form-control'}),
            'nombres' : forms.TextInput(attrs={'class':'form-control'}),
            'apellidos' : forms.TextInput(attrs={'class':'form-control'}),
        }

class Registroform(UserCreationForm):    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        ]
        labels = {
            'username' : 'Nombre de usuario',
            'first_name' : 'Nombre(s)',
            'last_name' : 'Apellido(s)',
            'email' : 'Correo electronico',
            'password':'Contraseña',
        }
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name','email', 'password1', 'password2']