from django.db import models
from django.core.exceptions import ValidationError
from socios.models import Socio
from datetime import date, timedelta


class Libro(models.Model):
    ESTADOS = [
        ("disponible", "Disponible"),
        ("prestado", "Prestado"),
        ("revision", "En revisión"),
    ]

    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=150)
    isbn = models.CharField(max_length=13, unique=True)
    editorial = models.CharField(max_length=100)
    año_publicacion = models.IntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default="disponible")
    fecha_alta = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Libro"
        verbose_name_plural = "Libros"
        ordering = ["titulo"]

    def __str__(self):
        return f"{self.titulo} - {self.autor}"

    def cambiar_estado(self, nuevo_estado):
        if nuevo_estado in dict(self.ESTADOS):
            self.estado = nuevo_estado
            self.save()
        else:
            raise ValidationError(f"Estado '{nuevo_estado}' no válido")

    @property
    def disponible(self):
        return self.estado == "disponible"


class Prestamo(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion_prevista = models.DateField()
    fecha_devolucion_real = models.DateField(null=True, blank=True)
    devuelto = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"
        ordering = ["-fecha_prestamo"]

    def __str__(self):
        return f"{self.libro.titulo} - {self.socio.nombre_completo}"

    @classmethod
    def registrar_prestamo(cls, socio, libro, fecha_devolucion=None):
        if not libro.disponible:
            raise ValidationError("El libro no está disponible")

        if fecha_devolucion:
            from datetime import datetime

            if isinstance(fecha_devolucion, str):
                fecha_devolucion = datetime.strptime(
                    fecha_devolucion, "%Y-%m-%d"
                ).date()
        else:
            fecha_devolucion = date.today() + timedelta(days=7)

        prestamo = cls.objects.create(
            libro=libro, socio=socio, fecha_devolucion_prevista=fecha_devolucion
        )
        libro.cambiar_estado("prestado")
        return prestamo

    def registrar_devolucion(self, buen_estado=True, importe_multa=None):
        self.fecha_devolucion_real = date.today()
        self.devuelto = True
        self.save()

        if buen_estado:
            self.libro.cambiar_estado("disponible")
        else:
            self.libro.cambiar_estado("revision")
            # Registrar multa si está dañado o vencido
            from multas.models import Multa
            from decimal import Decimal

            motivo = "Libro dañado" if not self.esta_vencido else "Devolución tardía"
            importe = Decimal(importe_multa) if importe_multa else None
            Multa.registrar_multa(self.socio, self.libro, motivo, importe)

    @property
    def dias_retraso(self):
        if self.devuelto or not self.fecha_devolucion_prevista:
            return 0
        return max(0, (date.today() - self.fecha_devolucion_prevista).days)

    @property
    def esta_vencido(self):
        return self.dias_retraso > 0
