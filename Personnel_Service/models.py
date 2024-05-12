from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser, PermissionsMixin
import random as rd

# Create your models here.
class ClubUserManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
 
        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **kwargs)
    
class Utilisateur(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length = 32,unique=True)
    nom=models.CharField(max_length=32,blank=True)
    prenom=models.CharField(max_length=50,blank=True)
    email = models.EmailField(blank=True,null=True,unique = True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_personnel = models.BooleanField(default = False)

    USERNAME_FIELD = 'username'

    objects = ClubUserManager()
    
    def __str__(self):

        return self.username

    
class Fonction(models.Model):
    nom_fonction = models.CharField(max_length = 32)

    def __str__(self):
        return self.nom_fonction


class Personnel(models.Model):
    user = models.ForeignKey(Utilisateur, on_delete = models.CASCADE)
    nom=models.CharField(max_length=32)
    prenom=models.CharField(max_length=32)
    genre=models.CharField(max_length=9)
    tel=models.CharField(max_length=9)
    email=models.EmailField(unique=True)
    fonction=models.ForeignKey(Fonction,on_delete = models.CASCADE)
    image=models.ImageField( upload_to='profil_personnel/', height_field=None, width_field=None, max_length=None,blank=True)
    identifiant = models.CharField(max_length = 30)
    
    def __str__(self):

        return f"{self.nom} {self.prenom}"
    


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
    def __str__(self):
        return self.nom_service


class Conge(models.Model):
    personnel = models.ForeignKey(Personnel, on_delete = models.CASCADE)
    debut_conge = models.DateTimeField()
    fin_conge = models.DateTimeField()
    motif = models.TextField()
    status_conge = models.BooleanField(default = False)








