from django.db import models

# Create your models here.

class RessourcesMateriel(models.Model):
    nom_materiel = models.CharField(max_length = 32 ,null = True)
    quantite = models.IntegerField()
    description = models.TextField()
    date_enreg = models.DateTimeField()
    service_materiel = models.CharField(max_length = 32, null = True)


class  Bloc(models.Model):
    nom_bloc = models.CharField(max_length = 32)
    nombre_sall = models.IntegerField()
    

class Salle(models.Model):
    num_bloc = models.ForeignKey(Bloc, on_delete = models.CASCADE)
    num_sall = models.IntegerField()
    capacite = models.IntegerField()

class Lit(models.Model):
    num_sall = models.ForeignKey(Salle, on_delete = models.CASCADE)
    num_lit = models.IntegerField()
    statut_lit = models.BooleanField(default = False, null = True)


class ProduitMedicaux(models.Model):
    nom_produit = models.CharField(max_length = 32)
    date_enreg = models.DateTimeField()
    date_exp = models.DateTimeField()
    quantite = models.IntegerField()










