from django.shortcuts import redirect, render
from datetime import datetime
from django.utils import timezone
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import get_user_model,login, logout, authenticate
from .models import *
from Patients.models import Patient,Satisfaction,Rendezvous,Consultation,FactureProduit
from django.contrib.auth.decorators import login_required
from News.models import Actualite
from Ressources.models import ProduitMedicaux

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

@login_required(login_url='/login')
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
        
        datetime_obj = timezone.make_aware(timezone.datetime.combine(date, time))
        existing_appointments = Rendezvous.objects.filter(personnel=doctor, date_rdv=date, heure_rdv=time)
        if existing_appointments.exists():
            # Si le créneau est pris, vous pouvez afficher un message d'erreur ou rediriger vers une autre page
            messages.error(request, 'Ce créneau est déjà pris. Veuillez choisir un autre.')
        
        # Vérifier si le créneau est dans le passé
        
        elif datetime_obj < timezone.now():
            # Si le créneau est dans le passé, affichez un message d'erreur
            messages.error(request, 'vous ne pouvez pas reserver dans le passé !')
        else:
        
        # Créer le rendez-vous
            appointment = Rendezvous.objects.create(personnel=doctor, patient=patient, date_rdv=date, heure_rdv=time,sujet_rdv= subjet)
            appointment.save()
        
            return redirect('home')  # Redirige vers la page de confirmation du rendez-vous
    
    error_messages = messages.get_messages(request)
    context['error_messages'] = error_messages
    
    return render(request, 'Personnel_Service/appointement.html',context)


def signup_user(request):
    if request.method == 'POST':
       prenom = request.POST.get('prenom')
       nom = request.POST.get('nom')
       genre = request.POST.get('genre')
       tel = request.POST.get('tel')
       email = request.POST.get('email')
       fonction = request.POST.get('fonction')
       password = request.POST.get('password')
       identifiant = f"{nom}{prenom}{rd.randint(1,999)}"
       
       user= Utilisateur.objects.create_user(username= identifiant, password=password,email=email,nom = nom,prenom = prenom)

       personnel = Personnel(user = user, identifiant = identifiant,
                        nom = nom,
                        prenom = prenom,
                        genre = genre,
                        telephone = tel,
                         
                        fonction = fonction,
                         )
       personnel.save()

       login(request,user)

       return redirect('login_personnel')
   
    return render(request,'Personnel_Service/register.html')

def login_user(request):
    if request.method == 'POST':
        username= request.POST.get('identifiant')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('home')
    return render(request,'Personnel_Service/login.html')
        


def logout_user(request):
    logout(request)
    return redirect('login_personnel')


#facturation pour l'achat des produits
# Dans views.py
@login_required
def liste_patient(request):
    utilisateur = request.user
    personnel = Personnel.objects.filter(user=utilisateur)
    if personnel is None:  # Vérifie si l'utilisateur est du personnel
        return HttpResponse('accès refusé')  # Redirige les patients vers une autre vue ou affiche un message d'erreur

    patients = Patient.objects.all()
    return render(request, 'Personnel_Service/liste_patients.html', {'patients': patients})


@login_required
def facturation_produits(request, patient_id):
      # Redirige les patients vers une autre vue ou affiche un message d'erreur

    # Récupérer la consultation du patient
    consultation = Consultation.objects.filter(patient_id=patient_id)

    # Récupérer les produits prescrits dans l'ordonnance
    produits_prescrits = ProduitMedicaux.objects.all()

    # Récupérer tous les produits disponibles en stock
    produits_stock = ProduitMedicaux.objects.all()

    if request.method == 'POST':
        # Récupérer les produits ajoutés au panier
        produits_ajoutés = request.POST.getlist('produits')

        # Calculer le montant total
        montant_total = sum([ProduitMedicaux.objects.get(id=produit_id).prix for produit_id in produits_ajoutés])

        # Créer une nouvelle facture pour les produits
        facture_produit = FactureProduit.objects.create(
            patient=consultation.patient,
            personnel=request.user,
            montant=montant_total
        )

        # Ajouter les produits à la facture
        facture_produit.produits.add(*produits_ajoutés)

        return HttpResponse('succès')  # Rediriger vers une page de succès ou une autre vue après la facturation

    return render(request, 'Personnel_Service/facture_produit.html', {'consultation': consultation, 'produits_prescrits': produits_prescrits, 'produits_stock': produits_stock})

login_required(login_url='/login')
def espace_personnel(request):
    
    
    
    return render(request,'Personnel_Service/index_Personnel.html')

def listePatients(request):
    liste_patients = Patient.objects.all()
    
    context = {
        'liste_patients':liste_patients
    }
    return render(request,'Personnel_Service/tables-data.html',context)

def userProfile(request):
    
    return render (request, 'Personnel_Service/users-profile.html')