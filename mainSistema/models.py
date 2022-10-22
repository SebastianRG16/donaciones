from django.db import models

# Create your models here.

class Asistente(models.Model):
    idAsistente = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    documento = models.CharField(max_length=100, verbose_name="Documento")
    telefono = models.CharField(max_length=10, verbose_name="telefono")
    tipo = models.CharField(max_length=100, verbose_name="tipo")
    correo = models.CharField(max_length=50, verbose_name="correo")
    

class Donacion(models.Model):
    idDonacion = models.AutoField(primary_key=True)
    tipo_donacion= models.CharField(max_length=45, verbose_name="tipo de donacion")
    Asistente_idAsistente = models.ForeignKey(Asistente, on_delete=models.CASCADE, null=True)
