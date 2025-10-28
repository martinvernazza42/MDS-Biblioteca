from django.urls import path
from . import views

app_name = 'libros'

urlpatterns = [
    path('', views.LibroListView.as_view(), name='lista'),
    path('crear/', views.LibroCreateView.as_view(), name='crear'),
    path('<int:pk>/', views.LibroDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.LibroUpdateView.as_view(), name='editar'),
    path('<int:pk>/prestar/', views.PrestarLibroView.as_view(), name='prestar'),
    path('<int:pk>/devolver/', views.DevolverLibroView.as_view(), name='devolver'),
    path('<int:pk>/cambiar-estado/', views.CambiarEstadoLibroView.as_view(), name='cambiar_estado'),
]