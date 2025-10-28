from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ROLES = [
        ("admin", "Administrador"),
        ("bibliotecario", "Bibliotecario"),
        ("asistente", "Asistente"),
    ]

    rol = models.CharField(max_length=20, choices=ROLES, default="asistente")
    telefono = models.CharField(max_length=15, blank=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_rol_display()})"

    def es_administrador(self):
        return self.rol == "admin"

    def puede_gestionar_socios(self):
        return self.rol in ["admin", "bibliotecario"]
