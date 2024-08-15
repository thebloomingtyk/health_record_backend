from django.shortcuts import render, redirect
# from .models import Doctor, Patient, Consultation
# from .forms import DoctorForm, PatientForm, ConsultationForm
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .models import Consultation


def home(request):
    return render(request, 'records/home.html')

# def add_doctor(request):
#     if request.method == 'POST':
#         form = DoctorForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = DoctorForm()
#     return render(request, 'records/add_doctor.html', {'form': form})

# def add_patient(request):
#     if request.method == 'POST':
#         form = PatientForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = PatientForm()
#     return render(request, 'records/add_patient.html', {'form': form})

# def add_consultation(request):
#     if request.method == 'POST':
#         form = ConsultationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = ConsultationForm()
#     return render(request, 'records/add_consultation.html', {'form': form})




def render_to_pdf(template_src, context_dict):
    template = render_to_string(template_src, context_dict)
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(template, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def daily_summary(request):
    consultations = Consultation.objects.all()
    context = {
        'consultations': consultations,
    }
    return render_to_pdf('records/daily_summary.html', context)



from rest_framework import viewsets
from .models import Room, Consultation
from .serializers import RoomSerializer, ConsultationSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer



from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Consultation
from datetime import datetime

def daily_summary_report(request):
    today = datetime.today().date()
    consultations = Consultation.objects.filter(consultation_time__date=today)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="daily_summary_{today}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica", 12)
    p.drawString(100, 750, f"Daily Summary Report - {today}")

    y = 700
    for consultation in consultations:
        p.drawString(100, y, f"Doctor: {consultation.doctor_name}, Patient: {consultation.patient_name}, Age: {consultation.patient_age}, Room: {consultation.room}, Treatment: {consultation.recommended_treatment}")
        y -= 20

    p.showPage()
    p.save()

    return response




# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .models import Consultation
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from datetime import datetime

class DailySummaryReportView(APIView):
    def get(self, request, format=None):
        # Get today's consultations
        today = datetime.today().date()
        consultations = Consultation.objects.filter(consultation_time__date=today)

        # Create PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="daily_summary.pdf"'

        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # Add title
        elements.append(Table([['Daily Summary Report']], colWidths=[6.5 * inch]))
        elements.append(Table([['Date:', today.strftime('%Y-%m-%d')]], colWidths=[6.5 * inch]))
        elements.append(Table([[' ']], colWidths=[6.5 * inch]))  # Add space

        # Create table data
        data = [['Doctor Name', 'Patient Name', 'Patient Age', 'Consultation Time', 'Room Number', 'Treatment Recommended']]
        
        for consultation in consultations:
            data.append([
                consultation.room.doctor_name,
                consultation.patient_name,
                consultation.patient_age,
                consultation.consultation_time.strftime('%Y-%m-%d %H:%M:%S'),
                consultation.room.room_number,
                consultation.recommended_treatment
            ])

        # Create table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(table)
        
        # Build PDF
        doc.build(elements)

        return response


from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Room

class RoomChoicesView(APIView):
    def get(self, request):
        room_choices = Room.ROOM_CHOICES
        data = [{"value": value, "label": label} for value, label in room_choices]
        return Response(data)