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
from operativos.models import Operativo
from django.views import generic

class ReportesOperativosListView(generic.ListView):
    model = Operativo
    template_name = 'sections/reportes/index.html'  # Specify your own template name/location

def header(canvas, doc):
    canvas.saveState()
    canvas.drawImage("static/img/bolivar.jpg", 60, 730, 90, 80,preserveAspectRatio=True)
    canvas.drawImage("static/img/transbolivar.png", 450, 730, 90, 80,preserveAspectRatio=True)
    canvas.restoreState()

def write_pdf_view(request):

    pk_operativo = request.POST.get("pk_operativo")
    operativo = Operativo.objects.get(pk=pk_operativo)

    doc = SimpleDocTemplate("/tmp/somefilename.pdf", pagesize=portrait(A4))
    Story = []
   
    ps = ParagraphStyle('parrafos',
                           alignment = TA_CENTER,
                           fontSize = 12,
                           fontName="Times-Roman")

    text = "<b>REPORTE DE ENTREGAS DE ALIMENTOS</b>"
    p = Paragraph(text, ps)
    Story.append(p)
    Story.append(Spacer(1,0.1*inch))
    
    text = "<b>Operativo: {{operativo.fecha}}</b>"
    p = Paragraph(text, ps)
    Story.append(p)
    Story.append(Spacer(1,0.3*inch))

    doc.build(Story, header)

    fs = FileSystemStorage("/tmp")
    with fs.open("somefilename.pdf") as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="somefilename.pdf"'
        return response

    return response