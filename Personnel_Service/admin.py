from django.contrib import admin
from .models import Personnel,Conge,Service, CalendrierPersonnel,Fonction,Utilisateur

import random as rd

class PersonnelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.identifiant:
            obj.identifiant = f"{obj.nom}{obj.prenom}{rd.randint(1, 999)}"
        super().save_model(request, obj, form, change)



admin.site.register(Personnel, PersonnelAdmin)
admin.site.register(Conge)
admin.site.register(Service)
admin.site.register(CalendrierPersonnel)
admin.site.register(Fonction)
admin.site.register(Utilisateur)