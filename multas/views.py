from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Multa


class MultaListView(ListView):
    model = Multa
    template_name = 'multas/lista.html'
    context_object_name = 'multas'
    paginate_by = 20

    def get_queryset(self):
        return Multa.objects.filter(pagada=False)


class MultaDetailView(DetailView):
    model = Multa
    template_name = 'multas/detalle.html'
    context_object_name = 'multa'


class PagarMultaView(View):
    def post(self, request, pk):
        try:
            multa = get_object_or_404(Multa, pk=pk)
            
            if multa.pagada:
                messages.warning(request, 'La multa ya está pagada')
                return redirect('multas:detalle', pk=pk)
            
            multa.marcar_como_pagada()
            messages.success(request, 'Multa pagada exitosamente')
            return redirect('multas:lista')
            
        except Exception as e:
            messages.error(request, f'Error al procesar pago: {str(e)}')
            return redirect('multas:detalle', pk=pk)