from django.db import models
from django.core.exceptions import ValidationError
from socios.models import Socio
from decimal import Decimal


class Multa(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE)
    libro_titulo = models.CharField(max_length=200, null=True, blank=True)
    importe = models.DecimalField(max_digits=6, decimal_places=2)
    fecha_multa = models.DateTimeField(auto_now_add=True)
    pagada = models.BooleanField(default=False)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    motivo = models.TextField()

    class Meta:
        verbose_name = "Multa"
        verbose_name_plural = "Multas"
        ordering = ['-fecha_multa']

    def __str__(self):
        return f"Multa {self.socio.nombre_completo} - {self.importe}€"

    @classmethod
    def registrar_multa(cls, socio, libro, motivo, importe=None):
        if not importe:
            importe = Decimal('5.00') if 'dañado' in motivo.lower() else Decimal('2.00')
        
        multa = cls.objects.create(
            socio=socio,
            libro_titulo=libro.titulo,
            importe=importe,
            motivo=motivo
        )
        return multa

    def marcar_como_pagada(self):
        from django.utils import timezone
        self.pagada = True
        self.fecha_pago = timezone.now()
        self.save()