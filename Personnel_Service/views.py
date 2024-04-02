from django.shortcuts import redirect, render
from datetime import datetime, time
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import *
from Patients.models import Patient,Satisfaction,Rendezvous
from News.models import Actualite

Utilisateur = get_user_model()
# Create your views here.
def home(request):
    
    nombre_personnel=Personnel.objects.count()
    nombre_service=Service.objects.count()
    nombre_patient=Patient.objects.count()
    services=Service.objects.all()
    temoignages= Satisfaction.objects.all()
    actualites=Actualite.objects.order_by("-date_publication")[:4]
    
    liste_informations=[]
    for service in services:
        info = service.information_personnel()
        liste_informations.append(info)
        
    
    
    context={
        'nombre_personnel': nombre_personnel,
        'nombre_service': nombre_service,
        'nombre_patient': nombre_patient,
        'services':services,
        'temoignages':temoignages,
        'liste_informations':liste_informations,
        'actualites':actualites,
        

        
        
    }
    return render(request,'Personnel_Service/index.html',context)


def make_appointement(request):
    services=Service.objects.all()
    doctors = Personnel.objects.all()
    
    liste_informations=[]
    for service in services:
        info = service.information_personnel()
        liste_informations.append(info)
        
    context ={
        'liste_informations':liste_informations,
        'doctors':doctors,
    }
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        patient = request.user
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        subjet = request.POST.get('subjet')
        doctor = Personnel.objects.get(id=doctor_id)
        
        date = datetime.strptime(date_str, '%Y-%m-%d').date()  # Convertir en objet datetime.date
        time = datetime.strptime(time_str, '%H:%M').time()  # Convertir en objet datetime.time
        
        
        existing_appointments = Rendezvous.objects.filter(personnel=doctor, date_rdv=date, heure_rdv=time)
        if existing_appointments.exists():
            # Si le créneau est pris, vous pouvez afficher un message d'erreur ou rediriger vers une autre page
            return render(request, 'appointment_error.html', {'error_message': 'Ce créneau est déjà pris. Veuillez choisir un autre.'})
        
        # Vérifier si le créneau est dans le passé
        datetime_obj = timezone.make_aware(timezone.datetime.combine(date, time))
        if datetime_obj < timezone.now():
            # Si le créneau est dans le passé, affichez un message d'erreur
            return render(request, 'appointment_error.html', {'error_message': 'Vous ne pouvez pas réserver un rendez-vous dans le passé.'})
        
        # Créer le rendez-vous
        appointment = Rendezvous.objects.create(personnel=doctor, patient=patient, date_rdv=date, heure_rdv=time,sujet_rdv= subjet)
        appointment.save()
        
        return redirect('home')  # Redirige vers la page de confirmation du rendez-vous
    
    else:
        doctor = request.POST.get('doctor')
        # Logique pour afficher les créneaux horaires disponibles du médecin
        # Par exemple, vous pouvez obtenir tous les rendez-vous du médecin pour cette date
        #existing_appointments = Rendezvous.objects.filter(doctor=doctor, date=date)
        # Ensuite, vous pouvez filtrer les créneaux horaires disponibles
        # Par exemple, si les rendez-vous ont lieu toutes les 30 minutes, vous pouvez exclure les créneaux déjà pris
        # et passer uniquement les créneaux disponibles au template
        #return render(request, 'book_appointment.html', {'doctor': doctor, 'existing_appointments': existing_appointments})
    
    return render(request, 'Personnel_Service/appointement.html',context)
