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
    
    def __str__(self):
        return self.nom_bloc

class Salle(models.Model):
    num_bloc = models.ForeignKey(Bloc, on_delete = models.CASCADE)
    num_sall = models.CharField(max_length = 32)
    capacite = models.IntegerField()
    
    def __str__(self):
        return self.num_sall

class Lit(models.Model):
    choix =[('libre','libre'),
            ('occupé','occupé')]
    num_sall = models.ForeignKey(Salle, on_delete = models.CASCADE)
    num_lit = models.IntegerField()
    statut_lit = models.CharField(max_length = 32,choices = choix,  default = 'libre')
    
    def __str__(self):
        return f"salle {self.num_sall} lit {self.num_lit}"


class ProduitMedicaux(models.Model):
    nom_produit = models.CharField(max_length = 32)
    date_enreg = models.DateTimeField(auto_now = True)
    date_exp = models.DateField()
    quantite = models.IntegerField()
    prix_unitaire = models.IntegerField()










