from django.views.generic import ListView, CreateView, DetailView, UpdateView, View, TemplateView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from datetime import date, timedelta
from .models import Libro, Prestamo
from socios.models import Socio


class LibroListView(ListView):
    model = Libro
    template_name = 'libros/lista.html'
    context_object_name = 'libros'
    paginate_by = 20


class LibroCreateView(CreateView):
    model = Libro
    template_name = 'libros/formulario.html'
    fields = ['titulo', 'autor', 'isbn', 'editorial', 'año_publicacion']
    success_url = reverse_lazy('libros:lista')

    def form_valid(self, form):
        isbn = form.cleaned_data.get('isbn')
        
        # Verificar si el ISBN ya existe
        try:
            libro_existente = Libro.objects.get(isbn=isbn)
            form.add_error('isbn', f'Ya existe un libro con este ISBN: {libro_existente.titulo} - {libro_existente.autor}')
            return self.form_invalid(form)
        except Libro.DoesNotExist:
            pass
        
        try:
            messages.success(self.request, 'Libro creado exitosamente')
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('isbn', 'Ya existe un libro con este ISBN')
            return self.form_invalid(form)


class LibroDetailView(DetailView):
    model = Libro
    template_name = 'libros/detalle.html'
    context_object_name = 'libro'


class LibroUpdateView(UpdateView):
    model = Libro
    template_name = 'libros/formulario.html'
    fields = ['titulo', 'autor', 'isbn', 'editorial', 'año_publicacion']
    success_url = reverse_lazy('libros:lista')


class PrestarLibroView(TemplateView):
    template_name = 'libros/prestar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['libro'] = get_object_or_404(Libro, pk=kwargs['pk'])
        context['socios'] = Socio.objects.filter(activo=True)
        return context
    
    def post(self, request, pk):
        try:
            libro = get_object_or_404(Libro, pk=pk)
            socio_id = request.POST.get('socio_id')
            socio = get_object_or_404(Socio, pk=socio_id)
            fecha_devolucion = request.POST.get('fecha_devolucion')
            
            # Usar el método del modelo para registrar préstamo
            prestamo = Prestamo.registrar_prestamo(socio, libro, fecha_devolucion)
            
            messages.success(request, f'Libro prestado a {socio.nombre_completo}. Devolución prevista: {prestamo.fecha_devolucion_prevista}')
            return redirect('libros:lista')
            
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('libros:prestar', pk=pk)
        except Exception as e:
            messages.error(request, f'Error al prestar libro: {str(e)}')
            return redirect('libros:prestar', pk=pk)


class DevolverLibroView(TemplateView):
    template_name = 'libros/devolver.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        libro = get_object_or_404(Libro, pk=kwargs['pk'])
        prestamo = Prestamo.objects.filter(libro=libro, devuelto=False).first()
        context['libro'] = libro
        context['prestamo'] = prestamo
        return context
    
    def post(self, request, pk):
        try:
            libro = get_object_or_404(Libro, pk=pk)
            prestamo = Prestamo.objects.filter(libro=libro, devuelto=False).first()
            
            if not prestamo:
                messages.error(request, 'No hay préstamo activo para este libro')
                return redirect('libros:lista')
            
            # Evaluar estado del libro
            buen_estado = request.POST.get('buen_estado') == 'si'
            importe = request.POST.get('importe')
            
            # Usar el método del modelo para registrar devolución
            prestamo.registrar_devolucion(buen_estado=buen_estado, importe_multa=importe)
            
            if buen_estado:
                messages.success(request, 'Libro devuelto exitosamente')
            else:
                messages.warning(request, 'Libro devuelto con daños. Se ha registrado una multa.')
            
            return redirect('libros:lista')
            
        except Exception as e:
            messages.error(request, f'Error al devolver libro: {str(e)}')
            return redirect('libros:devolver', pk=pk)


class CambiarEstadoLibroView(View):
    def post(self, request, pk):
        try:
            libro = get_object_or_404(Libro, pk=pk)
            nuevo_estado = request.POST.get('estado')
            
            libro.cambiar_estado(nuevo_estado)
            messages.success(request, f'Estado del libro cambiado a {libro.get_estado_display()}')
            
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error al cambiar estado: {str(e)}')
            
        return redirect('libros:lista')