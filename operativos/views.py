from django.shortcuts import render
from django.views import generic
from .models import Operativo
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import re


class OperativosListView(generic.ListView):
    model = Operativo
    template_name = 'sections/operativos/index.html'  # Specify your own template name/location

class OperativosCreateView(generic.CreateView):
    template_name = "sections/operativos/crear.html"

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        nbolsas = request.POST.get('nbolsas')
        proveedor = request.POST.get('proveedor')

        o = Operativo(nbolsas=nbolsas, proveedor=proveedor)
        o.save()

        messages.add_message(request, messages.SUCCESS, 'Operativo creado con exito')
        return redirect('operativos')


class OperativosDetailView(generic.View):
    template_name = "sections/operativos/admin.html"

    def get(self, request, *args, **kwargs):
        operativo = Operativo.objects.get(id=kwargs['pk'])
        context = {
            'operativo': operativo
        }
        return render(request, self.template_name, context)

class OperativosUpdateView(generic.View):
    template_name = "sections/beneficiarios/edit.html"

    def get(self, request, *args, **kwargs):
        cargos = Cargo.objects.all().order_by('nombre')
        beneficiarios = Beneficiarios.objects.get(cedula=kwargs['pk'])
        gerencias = Gerencia.objects.all()

        context = {
            'cargo': cargos, 
            'beneficiario': beneficiarios,
            'gerencias':gerencias
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        cedula = request.POST.get('cedula')
        nombres = request.POST.get('nombres')
        cargo = request.POST.get('cargo')
        status = request.POST.get('status')
        gerencia = request.POST.get('gerencia')

        try:
            b = Beneficiarios.objects.get(cedula=cedula)
        except Beneficiarios.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'No existe el beneficiario')
            return redirect('beneficiarios')
        
        if validcedula(cedula) != True:
            messages.add_message(request, messages.ERROR, 'La cedula no es valida')
            return redirect('beneficiarios_editar', pk=cedula)

        if len(nombres) < 2:
            messages.add_message(request, messages.ERROR, 'El nombre no es valido debe ser mayor a 2 digitos al menos')
            return redirect('beneficiarios_editar', pk=cedula)

        if cargo == '--------------------------':
            messages.add_message(request, messages.ERROR, 'El cargo no es valido')
            return redirect('beneficiarios_editar', pk=cedula)
        
        g = Gerencia.objects.get(pk=gerencia)

        b.cedula = cedula
        b.nombres = nombres
        b.cargo = cargo
        b.status = status
        b.gerencia = g
        b.save()

        messages.add_message(request, messages.SUCCESS, 'Beneficiario editado con exito')
        return redirect('beneficiarios')

def validcedula(cedula):
    if (re.match('\d', cedula) and (len(cedula) == 8 or len(cedula)== 7)):
        return True
    else:
        return False
        