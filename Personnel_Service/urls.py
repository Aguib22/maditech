"""
URL configuration for Medi_Tech project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path 
from Personnel_Service.views import *
 


urlpatterns = [
    path('',home,name='home'),
    path('rendez-vous/',make_appointement,name= 'rendez-vous'),
    path('service/',service,name='service'),
    path('apropos/',apropos,name='apropos'),
    path('contact/',contact,name='contact'),
    path('service/<int:id>',detail_service,name="detail_service"),
    path('liste/',liste_patient,name ='liste_patient'),
    #***************** personnel *****************************
    path('espace_personnel/',espace_personnel,name="espace_personnel"),
    path('listePatients/',listePatients,name ='listePatient'),
    path('user_profile/',userProfile,name = 'user_profile'),
    path('registers/',enregistrerPersonnel,name = 'registers'),
    path('pers_login/',login_personnel,name = 'connexion'),
    path('logout_personnel/',logout_personnel,name = 'logout_personnel'),
    #**********************patients********************************
    path('save_patient/',enregistrer_patient,name = 'save_patient'),
    path('consultation/',consultation,name ="consultation"),
    path('examen_labo/',examen, name ="examen_labo"),
    path('hospitalisation/', hospitalisation, name ='hospitalisation'),
    path('patients hospitalisés/', P_hospitalise, name ='p_hosp'),
    path('hosp/<int:id>/', detail_hospitalisation, name ='det_hosp'),
    

    
    
    path('facturation/<int:patient_id>/', facturation_produits, name='facturation_produits'),
    #********************** idrissa *************************
    
    

    
]