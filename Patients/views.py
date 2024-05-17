from django.conf import settings
import random as rd
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model,login,logout,authenticate,get_user_model
from django.contrib.auth.decorators import login_required

from django.urls import reverse
import pdfkit
import io
"""
#*****************************
import io
from django.http import FileResponse
from django.template.loader import render_to_string
from weasyprint import HTML
#*****************************
"""
from django.template.loader import get_template
from Personnel_Service.models import Personnel
from .models import Consultation, Examen, Patient
 

Utilisateur = get_user_model()

# Create your views here.

def login_user(request):
    if request.method == 'POST':
        username= request.POST.get('identifiant')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user:
            
            login(request,user)
            return redirect('home_patient')
        
    return render(request,'Patients/patient-login.html')
        


def logout_user(request):
    logout(request)
    return redirect('login')

def hom_patient(request):
    user = request.user
    
    if not user.is_personnel:
        patient = Patient.objects.get(user=user)
        consultation = Consultation.objects.get(patient = patient)
        context ={
        'patient':patient,
        'consultation':consultation
        }
        return render(request, 'Patients/espace_patient.html',context)
    else:
        return render(request,'Personnel_Service/page-error.html')
        
    
    
            
    
    
    
    
    
    return render(request, 'Patients/espace_patient.html',context)

def dm_patient(request):
    
    user = request.user
    
    patient = Patient.objects.get(user=user)
    consultation = Consultation.objects.get(patient = patient)
    examen = Examen.objects.get(patient= patient)

    context ={
        'patient':patient,
        'consultation':consultation,
        'examen':examen
        }
    return render(request,'Patients/dm_patient.html',context)

def dmePdf(request):
    user = request.user
    
    patient = Patient.objects.get(user=user)
    consultation = Consultation.objects.get(patient = patient)
    examen = Examen.objects.get(patient= patient)
    context ={
        'patient':patient,
        'consultation':consultation,
        'examen':examen
        }
    """
    # Create a file-like buffer to receive PDF data.

    # Create the PDF object, using the buffer as its "file."

    # Draw things on the PDF. Here we can draw the HTML content.

    # Step 1: Generate the HTML content from the template
    html_content = render_to_string('Patients/dme_pdf.html', context)  # Replace 'your_template.html' with the path to your template and 'your_data' with the data you want to pass to the template

    # Step 2: Create a file-like buffer to receive the PDF data.
    buffer = io.BytesIO()

    # Generate PDF from HTML content
    HTML(string=html_content).write_pdf(buffer)

    # Return the PDF as a FileResponse
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="hello.pdf")
    """
    config = pdfkit.configuration(wkhtmltopdf ="C:\\Users\\LIVE-TECH\\Desktop\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

    template = get_template('Patients/dme_pdf.html')
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding':'UTF-8',
        'enable-local-file-access':None
     }
    pdf = pdfkit.from_string(html,False,options=options,configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="dossier_medical.pdf"'
    return response
    
    
    