from django.urls import path
from . import views

app_name = 'socios'

urlpatterns = [
    path('', views.SocioListView.as_view(), name='lista'),
    path('crear/', views.SocioCreateView.as_view(), name='crear'),
    path('<int:pk>/', views.SocioDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.SocioUpdateView.as_view(), name='editar'),
    path('<int:pk>/eliminar/', views.SocioDeleteView.as_view(), name='eliminar'),
]