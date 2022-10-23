from django.db import models

# Create your models here.

class Asistente(models.Model):
    idAsistente = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    documento = models.CharField(max_length=100, verbose_name="Documento")
    telefono = models.CharField(max_length=10, verbose_name="telefono")
    correo = models.CharField(max_length=50, verbose_name="correo")
    tipo_aporte = models.CharField(max_length=50, verbose_name="tipo_aporte")
    tipo_persona = models.CharField(max_length=50, verbose_name="tipo_persona")

    class Meta:
        verbose_name = "Asistente"
        verbose_name_plural = "Asistentes"

    def __str__(self) -> str:
        return f"{self.nombres} - {self.tipo_persona}"
    
    

class Donacion(models.Model):
    idDonacion = models.AutoField(primary_key=True)
    tipo_donacion= models.CharField(max_length=45, verbose_name="tipo de donacion")
    Asistente_idAsistente = models.ForeignKey(Asistente, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Donacion"
        verbose_name_plural = "Donaciones"

    def __str__(self) -> str:
        return f"{self.tipo_donacion}"
