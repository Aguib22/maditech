from django.contrib import admin
from .models import RessourcesMateriel,Bloc,Salle,Lit,ProduitMedicaux

# Register your models here.
class AdminBloc(admin.ModelAdmin):
    list_display= ('nom_bloc','nombre_sall')
    search_fields =('nom_bloc','nombre_sall')

class AdminSalle(admin.ModelAdmin):
    list_display= ('num_bloc','num_sall','capacite')
    search_fields =('num_sall','capacite')  
    
class AdminLit(admin.ModelAdmin):
    list_display= ('num_sall','num_lit','statut_lit')
    search_fields =('num_lit','statut_lit') 
    
class AdminProduitMedicaux(admin.ModelAdmin):
    list_display= ('nom_produit','quantite','prix_unitaire','date_exp','date_enreg')
    search_fields =('nom_produit','prix_unitaire','date_exp','date_enreg')

admin.site.register(RessourcesMateriel),
admin.site.register(Bloc,AdminBloc),
admin.site.register(Salle,AdminSalle),
admin.site.register(Lit,AdminLit),
admin.site.register(ProduitMedicaux,AdminProduitMedicaux),
