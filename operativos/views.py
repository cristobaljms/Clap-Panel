from django.shortcuts import render
from django.views import generic
from .models import Operativo
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import re, json
from django.core.serializers import serialize
from beneficiarios.models import Beneficiarios, Gerencia
from operativos.models import Entrega

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
        soperativo = {
            'pk': operativo.id,
            'status' : operativo.status,
            'nbolsas' : operativo.nbolsas,
            'nbolsasForaneas' : operativo.nbolsasForaneas,
            'responsable' : operativo.responsable,
            'proveedor' : operativo.proveedor,
        }

        entregas = Entrega.objects.filter(operativo=operativo)

        beneficiarios = Beneficiarios.objects.all()
        sbeneficiarios = json.loads(serialize("json", beneficiarios))
        abeneficiarios = []
        nbentregadas = 0

        
        #sbeneficiarios_beneficiados = json.loads(serialize("json", beneficiarios_beneficiados))
        for b in sbeneficiarios:
            id = b['pk']
            nombres = b['fields']['nombres']
            gerencia = Gerencia.objects.get(pk=b['fields']['gerencia'])
            b_object = {
                'pk':id,
                'nombres':nombres,
                'gerencia': gerencia.nombre,
            }

            for entrega in entregas:
                if entrega.beneficiario.pk == id:
                    b_object['status'] = 1
                    nbentregadas = nbentregadas + entrega.nbolsas
            abeneficiarios.append(b_object)

        soperativo['nbentregadas'] = nbentregadas
        soperativo['nbrestantes'] = operativo.nbolsas - nbentregadas
        
        context = {
            'operativo': soperativo,
            'beneficiarios':abeneficiarios
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

class OperativoCerrarView(generic.DeleteView):
    template_name = "sections/operativos/cerrar.html"
    def get(self, request, *args, **kwargs):
        operativo = Operativo.objects.get(pk=kwargs['pk'])
        context = {
            'operativo': operativo
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        operativo = Operativo.objects.get(pk=kwargs['pk'])
        operativo.status = 0
        operativo.save()
        messages.add_message(request, messages.SUCCESS, 'Operativo cerrado')
        return redirect('operativos' )


class OperativoAbrirView(generic.DeleteView):
    template_name = "sections/operativos/abrir.html"
    def get(self, request, *args, **kwargs):
        operativo = Operativo.objects.get(pk=kwargs['pk'])
        context = {
            'operativo': operativo
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        operativo = Operativo.objects.get(pk=kwargs['pk'])
        operativo.status = 1
        operativo.save()
        messages.add_message(request, messages.SUCCESS, 'Operativo abierto')
        return redirect('operativos' )

class EntregaCreateView(generic.CreateView):
    template_name = "sections/operativos/entrega_especial.html"

    def get(self, request, *args, **kwargs):
        operativo = Operativo.objects.get(pk=kwargs['pk_operativo'])
        beneficiario = Beneficiarios.objects.get(pk=kwargs['pk_beneficiario'])

        context = {
            'operativo' : operativo,
            'beneficiario' : beneficiario
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pk_beneficiario = request.POST.get('pk_beneficiario')
        pk_operativo = request.POST.get('pk_operativo')
        nbolsas = request.POST.get('nbolsas')
        observacion = request.POST.get('observacion')
        comision = request.POST.get('comision')

        operativo = Operativo.objects.get(pk=pk_operativo)
        beneficiario = Beneficiarios.objects.get(pk=pk_beneficiario)

        if (comision == 'on'):
            e = Entrega(operativo=operativo,beneficiario=beneficiario, nbolsas=nbolsas, observacion=observacion, comision=1)
        else:
            e = Entrega(operativo=operativo,beneficiario=beneficiario, nbolsas=nbolsas, observacion=observacion)
        e.save()

        messages.add_message(request, messages.SUCCESS, 'Bolsa entregada a {}'.format(beneficiario.nombres))
        return redirect('operativos_administrar', pk=pk_operativo)


def handleEntregar(request, pk_operativo, pk_beneficiario):
    operativo = Operativo.objects.get(pk=pk_operativo)
    beneficiario = Beneficiarios.objects.get(pk=pk_beneficiario)
    entrega = Entrega(operativo=operativo, beneficiario=beneficiario)
    entrega.save()
    messages.add_message(request, messages.SUCCESS, 'Bolsa entregada a {}'.format(beneficiario.nombres))
    return redirect('operativos_administrar', pk=pk_operativo)


def validcedula(cedula):
    if (re.match('\d', cedula) and (len(cedula) == 8 or len(cedula)== 7)):
        return True
    else:
        return False
        