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
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('beneficiarios/', login_required(BeneficiariosListView.as_view(), login_url='/login/'), name='beneficiarios'),
    path('beneficiarios/crear', login_required(BeneficiariosCreateView.as_view(), login_url='/login/') , name='beneficiarios_crear'),
    path('beneficiarios/detalles/<int:pk>/', login_required(BeneficiarioDetailView.as_view(), login_url='/login/') , name='beneficiarios_detalles'),
    path('beneficiarios/editar/<int:pk>/', login_required(BeneficiariosUpdateView.as_view(), login_url='/login/') , name='beneficiarios_editar'),
    path('beneficiarios/eliminar/<int:pk>/', login_required(BeneficiarioDeleteView.as_view(), login_url='/login/') , name='beneficiarios_eliminar'),
    path('operativos/', login_required(OperativosListView.as_view(), login_url='/login/') , name='operativos'),
    path('operativos/crear', login_required(OperativosCreateView.as_view(), login_url='/login/') , name='operativos_crear'),
    path('operativos/admin/<int:pk>/', login_required(OperativosDetailView.as_view(), login_url='/login/') , name='operativos_administrar'),
    path('operativos/cerrar/<int:pk>/', login_required(OperativoCerrarView.as_view(), login_url='/login/') , name='operativos_cerrar'),
    path('operativos/abrir/<int:pk>/', login_required(OperativoAbrirView.as_view(), login_url='/login/') , name='operativos_abrir'),
    path('operativos/entregar/<int:pk_operativo>/<int:pk_beneficiario>/', login_required(handleEntregar, login_url='/login/') , name='operativos_entregar'),
    path('operativos/entregarespecial/<int:pk_operativo>/<int:pk_beneficiario>/', login_required(EntregaCreateView.as_view(), login_url='/login/') , name='operativos_entregar_especial'),
    path('reportes/', login_required(ReportesOperativosListView.as_view(), login_url='/login/') , name='reportes'),
    path('reportes/general/<int:pk_operativo>/', login_required(write_pdf_view, login_url='/login/') , name="reportes_generar"),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]