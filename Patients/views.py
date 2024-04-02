from django.conf import settings
import random as rd
from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model,login,logout,authenticate,get_user_model
from .models import Patient
 

Utilisateur = get_user_model()

# Create your views here.

def signup_user(request):
    if request.method == 'POST':
       prenom = request.POST.get('prenom')
       nom = request.POST.get('nom')
       genre = request.POST.get('genre')
       tel = request.POST.get('tel')
       email = request.POST.get('email')
       adresse = request.POST.get('adresse')
       password = request.POST.get('password')
       identifiant = f"{nom}{prenom}{rd.randint(1,999)}"
       
       patient = Patient(identifiant = identifiant,
                        nom = nom,
                         prenom = prenom,
                         genre = genre,
                         telephone = tel,
                         email = email,
                         adresse = adresse,
                         password = password)
       patient.save()

       user= Utilisateur.objects.create_user(username= identifiant, password=password,email=email)
       login(request,user)

       return redirect('login')
   
    return render(request,'Patients/register.html')

def login_user(request):
    if request.method == 'POST':
        username= request.POST.get('identifiant')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('home')
    return render(request,'Patients/login.html')
        


def logout_user(request):
    logout(request)
    return redirect('login')
