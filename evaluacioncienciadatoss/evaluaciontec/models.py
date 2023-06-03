from django.db import models

# Create your models here.
class departamentos(models.Model):
    idDepartamento= models.AutoField(db_column='idDepartamento', primary_key=True)
    nombre=models.CharField(db_column='nombre', max_length=60, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'departamentos'
        
class maestros(models.Model):
    idMaestro=models.AutoField(db_column='idMaestro', primary_key=True)
    plantel=models.CharField(db_column='plantel', max_length=60,blank=True, null=True)
    idDepartamento= models.ForeignKey('departamentos', models.DO_NOTHING,db_column='idDepartamento', blank=True, null=True)
    rfc=models.CharField(db_column='rfc', max_length=13,blank=True, null=True)
    curp=models.CharField(db_column='curp', max_length=19,blank=True, null=True)
    apellidoPaterno=models.CharField(db_column='apellidoPaterno', max_length=20, blank=True, null=True)
    apellidoMaterno=models.CharField(db_column='apellidoMaterno', max_length=20, blank=True, null=True)
    nombre=models.CharField(db_column='nombre', max_length=30, blank=True, null=True)
    email=models.CharField(db_column='email', max_length=40, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'maestros'
    
class carrera(models.Model):
    idCarrera=models.AutoField(db_column='idCarrera', primary_key=True)
    nombre=models.CharField(db_column='nombre', max_length=50, blank=True, null=True) 
    idDepartamento= models.ForeignKey('departamentos', models.DO_NOTHING,db_column='idDepartamento', blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'carrera'

class evaluaciondepartamento(models.Model):
    idEvaluacion=models.AutoField(db_column='idEvaluacion', primary_key=True)
    nombre=models.CharField(db_column='nombre', max_length=60,blank=True, null=True)
    promedio=models.DecimalField(db_column='promedio', max_digits=10, decimal_places=2)
    numeroAlumnos=models.IntegerField(db_column='numeroAlumnos', blank=True,null=True)
    aspectos= models.CharField(db_column='aspectos', max_length=60,blank=True, null=True) 
    puntaje=models.DecimalField(db_column='puntaje',max_digits=10, decimal_places=2)#models.CharField(db_column='puntaje', max_length=13,blank=True, null=True)
    calificacion=models.CharField(db_column='calificacion', max_length=30,blank=True, null=True)
    idDepartamento= models.ForeignKey('departamentos', models.DO_NOTHING,db_column='idDepartamento', blank=True, null=True)
    year= models.IntegerField(db_column='year', blank=True, null=True)
    semestre=models.CharField(db_column='semestre', max_length=40, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'evaluaciondepartamento'


class Usuario(models.Model):
    idU= models.AutoField(db_column='idU', primary_key=True)
    email = models.CharField(db_column='email', max_length=30, blank=True, null=True)
    nombres= models.CharField(db_column='nombres', max_length=20, blank=True, null=True)
    apellidos = models.CharField(db_column='apellidos', max_length=20, blank=True, null=True)  

    class Meta:
        managed = False
        db_table = 'usuarios'
# Create a new user

    
#user = User.objects.create_user(username='superusuario', password='SuperUsuarioEvalua',email="l17290882@cdguzman.tecnm.mx")
