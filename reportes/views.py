from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from operativos.models import Operativo, Entrega
from beneficiarios.models import Beneficiarios
from django.views import generic

class ReportesOperativosListView(generic.ListView):
    model = Operativo
    template_name = 'sections/reportes/index.html'  # Specify your own template name/location

def header(canvas, doc):
    canvas.saveState()
    canvas.drawImage("static/img/bolivar.jpg", 40, 760, 90, 80,preserveAspectRatio=True)
    canvas.drawImage("static/img/transbolivar.png", 130, 775, 70, 60,preserveAspectRatio=True)
    canvas.restoreState()

def write_pdf_view(request, pk_operativo):

    #pk_operativo = request.POST.get("pk_operativo")
    operativo = Operativo.objects.get(pk=pk_operativo)
    entregas = Entrega.objects.filter(operativo=pk_operativo)

    doc = SimpleDocTemplate("/tmp/somefilename.pdf", pagesize=portrait(A4))
    Story = []
   
    ps = ParagraphStyle('parrafos',
                           alignment = TA_CENTER,
                           fontSize = 12,
                           fontName="Times-Roman")

    text = "<b>REPORTE DE ENTREGAS DE ALIMENTOS</b>"
    p = Paragraph(text, ps)
    Story.append(p)
    Story.append(Spacer(1,0.5*inch))
    
    ps = ParagraphStyle('parrafos',
                           alignment = TA_JUSTIFY,
                           fontSize = 10,
                           fontName="Times-Roman")

    #__________________________________________--

    text = "<b>Fecha: </b>{}".format(operativo.fecha)
    p = Paragraph(text, ps)
    Story.append(p)
    Story.append(Spacer(1,0.05*inch))
    text = "<b>Proveedor: </b>{}".format(operativo.proveedor)
    p = Paragraph(text, ps)
    Story.append(p)
    Story.append(Spacer(1,0.05*inch))
    text = "<b>Responsable: </b>{}".format(operativo.responsable)
    p = Paragraph(text, ps)
    Story.append(p)
    Story.append(Spacer(1,0.05*inch))
    text = "<b>Bolsas recibidas: </b>{} <b>Bolsas entregadas: </b>{} <b>Bolsas sobrantes: </b>{}".format(operativo.nbolsas, operativo.nbolsas, operativo.nbolsas)
    p = Paragraph(text, ps)
    Story.append(p)
    Story.append(Spacer(1,0.4*inch))

    ps = ParagraphStyle('parrafos',
                           alignment = TA_JUSTIFY,
                           fontSize = 11,
                           fontName="Times-Roman")

    text = "<b>Beneficiarios especiales: </b>"
    p = Paragraph(text, ps)
    Story.append(p)
    Story.append(Spacer(1,0.2*inch))

    ps = ParagraphStyle('parrafos',
                           alignment = TA_JUSTIFY,
                           fontSize = 10,
                           fontName="Times-Roman")

    nentregas = 0
    for entrega in entregas:
        if (entrega.especial == 1):
            beneficiario = Beneficiarios.objects.get(pk=entrega.beneficiario.pk)
            text = "{} - {}".format(entrega.nbolsas, beneficiario.nombres)
            p = Paragraph(text, ps)
            Story.append(p)
            Story.append(Spacer(1,0.05*inch))
            nentregas = nentregas + entrega.nbolsas

    ps = ParagraphStyle('parrafos',
                           alignment = TA_JUSTIFY,
                           fontSize = 11,
                           fontName="Times-Roman")

    text = " "
    p = Paragraph(text, ps)
    Story.append(p)
    Story.append(Spacer(1,0.2*inch))

    text = "<b> Listado de Beneficiarios: </b>"
    p = Paragraph(text, ps)
    Story.append(p)
    Story.append(Spacer(1,0.2*inch))

    ps = ParagraphStyle('parrafos',
                           alignment = TA_JUSTIFY,
                           fontSize = 10,
                           fontName="Times-Roman")

    nentregas = 0
    for entrega in entregas:
        if (entrega.especial == 0):
            beneficiario = Beneficiarios.objects.get(pk=entrega.beneficiario.pk)
            text = "{} - {}".format(entrega.nbolsas, beneficiario.nombres)
            p = Paragraph(text, ps)
            Story.append(p)
            Story.append(Spacer(1,0.05*inch))
            nentregas = nentregas + entrega.nbolsas

    doc.build(Story, header)

    fs = FileSystemStorage("/tmp")
    with fs.open("somefilename.pdf") as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="somefilename.pdf"'
        return response

    return response