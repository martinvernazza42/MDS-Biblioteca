from django.urls import path
from . import views

app_name = 'multas'

urlpatterns = [
    path('', views.MultaListView.as_view(), name='lista'),
    path('<int:pk>/', views.MultaDetailView.as_view(), name='detalle'),
    path('<int:pk>/pagar/', views.PagarMultaView.as_view(), name='pagar'),
]