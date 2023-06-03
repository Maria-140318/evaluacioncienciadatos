from django.contrib import admin
from .models import departamentos, carrera,maestros, evaluaciondepartamento
# Register your models here.

admin.site.register(departamentos)
admin.site.register(carrera)
admin.site.register(maestros)
admin.site.register(evaluaciondepartamento)

