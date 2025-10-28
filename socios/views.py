from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import IntegrityError
from .models import Socio


class SocioListView(ListView):
    model = Socio
    template_name = "socios/lista.html"
    context_object_name = "socios"
    paginate_by = 20


class SocioCreateView(CreateView):
    model = Socio
    template_name = "socios/formulario.html"
    fields = ["nombre", "apellidos", "dni", "email", "telefono", "direccion"]
    success_url = reverse_lazy("socios:lista")

    def form_valid(self, form):
        dni = form.cleaned_data.get("dni")

        # Verificar si el socio ya existe
        try:
            socio_existente = Socio.objects.get(dni=dni)
            form.add_error(
                "dni",
                f"Ya existe un socio con este DNI: {socio_existente.nombre_completo} (Número: {socio_existente.numero_socio})",
            )
            return self.form_invalid(form)
        except Socio.DoesNotExist:
            pass

        try:
            response = super().form_valid(form)
            messages.success(
                self.request,
                f"Socio creado exitosamente. Número de socio: {self.object.numero_socio}",
            )
            return response
        except IntegrityError:
            form.add_error("dni", "Ya existe un socio con este DNI")
            return self.form_invalid(form)


class SocioDetailView(DetailView):
    model = Socio
    template_name = "socios/detalle.html"
    context_object_name = "socio"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from libros.models import Prestamo

        context["prestamos_activos"] = Prestamo.objects.filter(
            socio=self.object, devuelto=False
        ).select_related("libro")
        return context


class SocioUpdateView(UpdateView):
    model = Socio
    template_name = "socios/formulario.html"
    fields = ["nombre", "apellidos", "dni", "email", "telefono", "direccion"]
    success_url = reverse_lazy("socios:lista")

    def form_valid(self, form):
        messages.success(self.request, "Socio actualizado exitosamente")
        return super().form_valid(form)


class SocioDeleteView(DeleteView):
    model = Socio
    template_name = "socios/confirmar_eliminacion.html"
    success_url = reverse_lazy("socios:lista")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Socio eliminado exitosamente")
        return super().delete(request, *args, **kwargs)
