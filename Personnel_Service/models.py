from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser, PermissionsMixin
import random as rd

# Create your models here.
class User(BaseUserManager):
    def create_user(self,username,email,password=None,**kwargs):
        user=self.model(email=email,username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,username,email,password=None,**kwargs):
        kwargs.setdefault("is_staff",True)
        kwargs.setdefault("is_superuser",True)
        return self.create_user(username,email,password,**kwargs)
    
class Utilisateur(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length = 32)
    nom=models.CharField(max_length=32,blank=True)
    prenom=models.CharField(max_length=50,blank=True)
    email = models.EmailField(unique = True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    
    USERNAME_FIELD="email"
    objects=User()
    def __str__(self):

        return self.email

    
class Fonction(models.Model):
    nom_fonction = models.CharField(max_length = 32)

    def __str__(self):
        return self.nom_fonction


class Personnel(models.Model):
    nom=models.CharField(max_length=32)
    prenom=models.CharField(max_length=32)
    genre=models.CharField(max_length=9)
    tel=models.CharField(max_length=9)
    email=models.EmailField(unique=True)
    fonction=models.ForeignKey(Fonction,on_delete = models.CASCADE)
    image=models.ImageField( upload_to='profil_personnel/', height_field=None, width_field=None, max_length=None,blank=True)
    identifiant = models.CharField(max_length = 32,unique= True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    def __str__(self):

        return f"{self.nom} {self.prenom}"

    def genere_identifiant(self):
        return f"{self.nom}{self.prenom}{rd.randint(1,999)}"
    

    def save(self,*args,**kwargs):
        if not self.identifiant:
            self.identifiant = self.genere_identifiant()
        super().save(*args,**kwargs)
    
    


class CalendrierPersonnel(models.Model):
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    horaire = models.TimeField()
    personnel = models.ForeignKey(Personnel,on_delete = models.CASCADE)




class Service(models.Model):
    nom_service = models.CharField(max_length = 32)
    description = models.TextField()
    image=models.ImageField(upload_to='image_service/', height_field=None, width_field=None, max_length=None,blank=True)
    responsable = models.ForeignKey(Personnel,on_delete = models.CASCADE)
    
    def information_personnel(self):
        
        
        return {
                'nom': self.responsable.nom,
                'prenom': self.responsable.prenom,
                'fonction': self.responsable.fonction,
                'image': self.responsable.image,
                
                
            }


class Conge(models.Model):
    personnel = models.ForeignKey(Personnel, on_delete = models.CASCADE)
    debut_conge = models.DateTimeField()
    fin_conge = models.DateTimeField()
    motif = models.TextField()
    status_conge = models.BooleanField(default = False)








