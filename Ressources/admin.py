from django.contrib import admin
from .models import RessourcesMateriel,Bloc,Salle,Lit,ProduitMedicaux

# Register your models here.
admin.site.register(RessourcesMateriel),
admin.site.register(Bloc),
admin.site.register(Salle),
admin.site.register(Lit),
admin.site.register(ProduitMedicaux),
