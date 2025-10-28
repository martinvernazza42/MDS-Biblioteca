from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class LoginView(DjangoLoginView):
    template_name = 'usuarios/login.html'
    success_url = reverse_lazy('libros:lista')


class LogoutView(DjangoLogoutView):
    next_page = reverse_lazy('usuarios:login')


class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = 'usuarios/perfil.html'
    login_url = reverse_lazy('usuarios:login')