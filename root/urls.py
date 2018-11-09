"""root URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import index, login, beneficiarios, operativos, reportes
from beneficiarios.views import BeneficiarioDetailView,BeneficiariosListView, BeneficiariosCreateView, BeneficiariosUpdateView, BeneficiarioDeleteView
from operativos.views import EntregaCreateView ,OperativosListView, OperativosCreateView, OperativosDetailView, handleEntregar, OperativoCerrarView, OperativoAbrirView
from reportes.views import write_pdf_view, ReportesOperativosListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('beneficiarios/', BeneficiariosListView.as_view(), name='beneficiarios'),
    path('beneficiarios/crear', BeneficiariosCreateView.as_view(), name='beneficiarios_crear'),
    path('beneficiarios/detalles/<int:pk>/', BeneficiarioDetailView.as_view(), name='beneficiarios_detalles'),
    path('beneficiarios/editar/<int:pk>/', BeneficiariosUpdateView.as_view(), name='beneficiarios_editar'),
    path('beneficiarios/eliminar/<int:pk>/', BeneficiarioDeleteView.as_view(), name='beneficiarios_eliminar'),
    path('operativos/', OperativosListView.as_view(), name='operativos'),
    path('operativos/crear', OperativosCreateView.as_view(), name='operativos_crear'),
    path('operativos/admin/<int:pk>/', OperativosDetailView.as_view(), name='operativos_administrar'),
    path('operativos/cerrar/<int:pk>/', OperativoCerrarView.as_view(), name='operativos_cerrar'),
    path('operativos/abrir/<int:pk>/', OperativoAbrirView.as_view(), name='operativos_abrir'),
    path('operativos/entregar/<int:pk_operativo>/<int:pk_beneficiario>/', handleEntregar, name='operativos_entregar'),
    path('operativos/entregarespecial/<int:pk_operativo>/<int:pk_beneficiario>/', EntregaCreateView.as_view(), name='operativos_entregar_especial'),
    path('reportes/', ReportesOperativosListView.as_view(), name='reportes'),
    path('reportes/general/<int:pk_operativo>/', write_pdf_view, name="reportes_generar"),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]