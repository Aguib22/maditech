from django.db import models

from Personnel_Service.models import Personnel,Service,Utilisateur
from Ressources.models import Lit
import random as rd

# Create your models here.

class Patient(models.Model):
    user = models.ForeignKey(Utilisateur, on_delete = models.CASCADE)
    nom = models.CharField(max_length = 32)
    prenom = models.CharField(max_length = 32)
    genre = models.CharField(max_length = 9)
    telephone = models.CharField(max_length = 10)
    email = models.EmailField(max_length = 32)
    profil_patient=models.ImageField(upload_to='profil_patient/', height_field=None, width_field=None, max_length=None, blank=True)
    adresse = models.CharField(max_length = 30)
    password = models.CharField(max_length=32 )
    identifiant = models.CharField(max_length = 30)
    date_enrgistrement = models.DateField(auto_now = True)

    def __str__(self):

        return f"{self.nom} {self.prenom}"

    

class Rendezvous(models.Model):
    status = [
        ("confirmé","confirmé"),
        ("en attente","en attente"),
        ("annulé","annulé")
    ]
    date_rdv = models.DateField()
    heure_rdv = models.TimeField()
    sujet_rdv = models.TextField(blank= True,null = True)
    patient = models.ForeignKey(Utilisateur,on_delete = models.CASCADE)
    personnel = models.ForeignKey(Personnel,on_delete = models.CASCADE)
    status_rdv = models.CharField(max_length = 32,choices = status, default = "en attente")


class TypeAnalyse(models.Model):
    nom_analyse = models.CharField(max_length = 32)
    dure_analyse = models.DateTimeField()
    prix_analyse = models.IntegerField()


class Examen(models.Model):
    type_analyse = models.ForeignKey(TypeAnalyse,on_delete = models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    resultat_examen = models.CharField(max_length =128)
    date_examen = models.DateTimeField()
    laborantain = models.ForeignKey(Personnel,on_delete = models.CASCADE)


class Satisfaction(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    contenu = models.TextField()
    date = models.DateTimeField()


class FactureSoins(models.Model):
    type_traitement = models.CharField(max_length = 32)
    montant = models.IntegerField()
    date_facture = models.DateTimeField()
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    personnel = models.ForeignKey(Personnel, on_delete = models.CASCADE)



class FactureProduit(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    date_factureproduit =  models.DateTimeField()
    personnel = models.ForeignKey(Personnel, on_delete = models.CASCADE)
    montant = models.IntegerField()


class DossierMedicaux(models.Model):
    traitement = models.CharField(max_length = 128)
    antecedant = models.CharField(max_length = 128)
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)


class Hospitalisation(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    num_lit = models.ForeignKey(Lit, on_delete = models.CASCADE)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    motif = models.CharField(max_length = 128)
    service = models.ForeignKey(Service , on_delete = models.CASCADE)


class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE)
    personnel = models.ForeignKey(Personnel, on_delete = models.CASCADE)
    poid = models.DecimalField(max_digits = 2,decimal_places =2)
    temperature = models.DecimalField(max_digits = 2,decimal_places =2)
    tension = models.IntegerField()
    age = models.IntegerField()
    taille = models.DecimalField(max_digits = 2,decimal_places =2)
    plainte = models.CharField(max_length = 128)
    diagnostic = models.CharField(max_length = 128)
    prescription = models.CharField(max_length = 128)
    date_consultation = models.DateTimeField()














    
    




    
    


