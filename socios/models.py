from django.db import models
from django.core.exceptions import ValidationError
import uuid


class Socio(models.Model):
    numero_socio = models.CharField(max_length=20, unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    dni = models.CharField(max_length=9, unique=True)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()
    fecha_alta = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Socio"
        verbose_name_plural = "Socios"
        ordering = ['apellidos', 'nombre']

    def __str__(self):
        return f"{self.numero_socio} - {self.apellidos}, {self.nombre}"

    def save(self, *args, **kwargs):
        if not self.numero_socio:
            self.numero_socio = str(uuid.uuid4())[:8].upper()
        super().save(*args, **kwargs)

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellidos}"

    @classmethod
    def existe_socio(cls, dni):
        return cls.objects.filter(dni=dni).exists()