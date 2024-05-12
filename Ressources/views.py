from django.shortcuts import render

from Ressources.models import ProduitMedicaux

# Create your views here.
def liste_produit(request):
    produits = ProduitMedicaux.objects.all().order_by('-date_enreg')
    if request.method == 'POST':
        nom_prod = request.POST.get('nom_prod')
        prix_unit =request.POST.get('pu')
        qte = request.POST.get('qte')
        d_peremption = request.POST.get('d_peremption')
        
        produit = ProduitMedicaux.objects.create(nom_produit = nom_prod,
                                                 prix_unitaire =prix_unit,
                                                 quantite = qte,
                                                 date_exp = d_peremption)
        produit.save()
    
    return render(request,'Ressources/produits.html',{'produits':produits})

