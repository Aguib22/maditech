from django.shortcuts import redirect, render
from datetime import datetime
from django.utils import timezone
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import get_user_model,login, logout, authenticate
from .models import *
from Patients.models import Examen, Patient,Satisfaction,Rendezvous,Consultation,FactureProduit,TypeAnalyse,Hospitalisation
from django.contrib.auth.decorators import login_required
from News.models import Actualite
from Ressources.models import ProduitMedicaux,Lit
from .models import Fonction

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
    return render(request,'Personnel_Service/indexs.html',context)

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

#*********************************************************************

def service(request):
    services = Service.objects.all()
    context ={
        'services':services
    }
    
    return render(request,'Personnel_Service/service.html',context)

def detail_service(request,id):
    service=Service.objects.get(pk=id)
    context={
        'service':service
    }
    
    return render(request, 'Personnel_Service/detail_service.html',context)

#fonction qui retourne la page apropos
def apropos(request):
    return render(request,'Personnel_Service/apropos.html')

def contact(request):
    return render(request,'Personnel_Service/contact.html')
#*********************************************************************


def enregistrerPersonnel(request):
    if not request.user.is_superuser:
        
        return render(request,'Personnel_Service/pages-error-404.html')
    
    fonctions = Fonction.objects.all()
    if request.method == 'POST':
       prenom = request.POST.get('prenom')
       nom = request.POST.get('nom')
       genre = request.POST.get('genre')
       tel = request.POST.get('tel')
       email = request.POST.get('email')
       fonct = request.POST.get('fonction')
       password = request.POST.get('password')
       identifiant = f"{nom}{prenom}{rd.randint(1,999)}"
       fonction = Fonction.objects.get(id = fonct)
       user= Utilisateur.objects.create_user(username= identifiant, password=password,email=email,nom = nom,prenom = prenom)

       personnel = Personnel(user = user, identifiant = identifiant,
                        nom = nom,
                        prenom = prenom,
                        genre = genre,
                        tel = tel,
                        email =email, 
                        fonction = fonction,
                         )
       personnel.save()

       return redirect('espace_personnel')
   
    return render(request,'Personnel_Service/pages-register.html',{'fonctions':fonctions})

def login_personnel(request):
    if request.method == 'POST':
        username= request.POST.get('identifiant')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user:
            if user.is_personnel:
                login(request,user)
                return redirect('espace_personnel')
                
            else:
                return render(request,'Personnel_Service/page-error.html')
        
            
    return render(request,'Personnel_Service/pages-login.html')
        


def logout_personnel(request):
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

login_required(login_url='/connexion')
def espace_personnel(request):
    nombre_personnel=Personnel.objects.count()
    nombre_service=Service.objects.count()
    nombre_patient=Patient.objects.count()
    context ={
        'nombre_personnel':nombre_personnel,
        'nombre_service':nombre_service,
        'nombre_patient':nombre_patient
    }
    if request.user.is_personnel:
    
        return render(request,'Personnel_Service/index_Personnel.html',context)
    else:
        return render(request,'Personnel_Service/page-error.html')
    
def listePatients(request):
    liste_patients = Patient.objects.all()
    
    context = {
        'liste_patients':liste_patients,
        
    }
    return render(request,'Personnel_Service/tables-data.html',context)

def userProfile(request):
    user = request.user
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        genre = request.POST.get('genre')
        fonction = request.POST.get('fonction')
        tel = request.POST.get('tel')
        email = request.POST.get('email')

        user2=Utilisateur.objects.get(id=user.id)
        user2.nom=nom
        user2.prenom=prenom
        user2.email=email
        user2.save()
        user3=Personnel.objects.get(user=user2)
        user3.nom=nom
        user3.prenom=prenom
        user3.genre=genre
        user3.tel=tel
        user3.email=email
        user3.save()

        
    personnel = Personnel.objects.get(user=user)
    context = {
        'personnel':personnel
    }
    return render (request, 'Personnel_Service/users-profile.html',context)

# ************* gestion du Patient ***************************

def enregistrer_patient(request):
   liste_patients = Patient.objects.order_by("-date_enrgistrement")
    
   context = {
        'liste_patients':liste_patients
    }
   if request.method == "POST":
       
       prenom = request.POST.get('prenom')
       nom = request.POST.get('nom')
       genre = request.POST.get('genre')
       tel = request.POST.get('tel')
       email = request.POST.get('email')
       adresse = request.POST.get('adresse')
       
       password = "meditech"
       identifiant = f"{nom}{prenom}{rd.randint(1,999)}"
       
       
       user= Utilisateur.objects.create_user(username= identifiant, password=password,email=email,nom = nom,prenom = prenom)

       patient = Patient(user = user, identifiant = identifiant,
                        nom = nom,
                         prenom = prenom,
                         genre = genre,
                         telephone = tel,
                         email = email,
                         adresse = adresse,
                         )
       patient.save()

    
   return render(request, 'Personnel_Service/enregistrer_patient.html',context)


def consultation(request):
    patients = Patient.objects.all().order_by("-date_enrgistrement")
    context= {
        'patients':patients,
    }

    if request.method == 'POST':

        user = request.user
        patient_id = request.POST.get('patient')
        poid = request.POST.get('poids')
        temperature = request.POST.get('temp')
        tension = request.POST.get('tension')
        age = request.POST.get('age')
        taille = request.POST.get('taille')
        plainte =request.POST.get('plainte')
        diagnostic = request.POST.get('diagnostic')
        prescription = request.POST.get('prescription')
        patient = Patient.objects.get(identifiant =patient_id)
        personnel = Personnel.objects.get(user=user)
        consultation = Consultation.objects.create(personnel = personnel, patient = patient,
            poid = poid,temperature = temperature,tension = tension, age = age,
            taille = taille, plainte = plainte, diagnostic = diagnostic, prescription = prescription
        )

        consultation.save()
    return render (request, 'Personnel_Service/consultation.html',context)

def examen(request):
    analyses = TypeAnalyse.objects.all()
    patients = Patient.objects.all().order_by("-date_enrgistrement")
    context = {
        'analyses':analyses,
        'patients':patients,
    }
    if request.method == 'POST':
        personnel = request.user
        patient_id = request.POST.get('patient')
        exam = request.POST.get('typeanalyse')
        rest = request.POST.get('resultat')
        patient = Patient.objects.get(identifiant = patient_id)
        examen = TypeAnalyse.objects.get(id=exam)
        tarif = examen.prix_analyse
        laborantain = Personnel.objects.get(user=personnel)
        examens = Examen.objects.create(laborantain=laborantain,
                                             patient = patient,
                                             type_analyse = examen,
                                             resultat_examen =rest,
                                             tarif =tarif)
        examens.save()
        
    return render(request, 'Personnel_Service/examen.html',context)

def hospitalisation(request):
    liste_patients = Patient.objects.order_by("-date_enrgistrement")
    lits = Lit.objects.filter(statut_lit="libre")
    services = Service.objects.all()
    context= {
        'lits':lits,
        'services':services,
        'liste_patients':liste_patients   
    }
    if request.method == "POST":
        patient_id = request.POST.get('patient')
        service_id = request.POST.get('service')
        lit_id = request.POST.get('lit')
        debut = request.POST.get('debut')
        fin = request.POST.get('fin')
        motif = request.POST.get('motif')
        
        service = Service.objects.get(id = service_id)
        lit = Lit.objects.get(id = lit_id)
        lit.statut_lit = "occupé"
        lit.save()
        patient = Patient.objects.get(identifiant = patient_id)
        
        hospitalisation = Hospitalisation.objects.create(
            patient = patient,
            service = service,
            num_lit = lit,
            date_debut = debut,
            date_fin = fin,
            motif = motif
            
        )
        hospitalisation.save()
                
    return render(request, 'Personnel_Service/hospitalisation.html',context)

def P_hospitalise(request):
    patient_hospitalise = Hospitalisation.objects.all().order_by("-date_enregistrement")
    context={
        'patient_hospitalise':patient_hospitalise
    }
    return render(request,'Personnel_Service/p_hospitalise.html',context)

def detail_hospitalisation(request,id):
    hosp = Hospitalisation.objects.get(pk=id)
    
    return render(request,'Personnel_Service/det_hosp.html',{'hosp':hosp})





