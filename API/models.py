from django.db import models

class Carrera(models.Model):
    id = models.AutoField(primary_key=True)  
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Alumno(models.Model):
    id = models.AutoField(primary_key=True) 
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    carrera = models.ForeignKey(Carrera, related_name='alumnos', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"