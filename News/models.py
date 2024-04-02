from django.db import models

# Create your models here.

class Chat(models.Model):
    emeteur = models.CharField(max_length = 128)
    recepteur = models.CharField(max_length = 128)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now =True)



class Actualite(models.Model):
    titre = models.CharField(max_length = 32)
    image = models.ImageField()
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now =True)
    
    
