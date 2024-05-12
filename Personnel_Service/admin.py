from django.contrib import admin
from .models import Personnel,Conge,Service, CalendrierPersonnel,Fonction,Utilisateur

import random as rd
admin.site.site_header = "MediTech"
admin.site.site_title = "meditech"
admin.site.index_title ="Admin MediTech"

class PersonnelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.identifiant:
            obj.identifiant = f"{obj.nom}{obj.prenom}{rd.randint(1, 999)}"
        super().save_model(request, obj, form, change)

class AdminPersonnel(admin.ModelAdmin):
    list_display= ('identifiant','nom','prenom','email','tel')
    search_fields =('identifiant','nom','email')
    
class AdminConge(admin.ModelAdmin):
    list_display= ('personnel','debut_conge','fin_conge','motif','status_conge')
    search_fields =('personnel','debut_conge','fin_conge','motif','status_conge')

class AdminService(admin.ModelAdmin):
    list_display= ('nom_service','responsable')
    search_fields =('nom_service','responsable')
    
class AdminCalendrierPersonnel(admin.ModelAdmin):
    list_display= ()
    search_fields =()
    
class AdminUtilisateur(admin.ModelAdmin):
    list_display= ('username','nom','prenom','email')
    search_fields =('username','nom','prenom','email')
    
class AdminPersonnel(admin.ModelAdmin):
    list_display= ('identifiant','nom','prenom','email','fonction','tel')
    search_fields =('identifiant','nom','email')

admin.site.register(Personnel, AdminPersonnel)
admin.site.register(Conge,AdminConge)
admin.site.register(Service,AdminService)
admin.site.register(CalendrierPersonnel)
admin.site.register(Fonction)
admin.site.register(Utilisateur,AdminUtilisateur)