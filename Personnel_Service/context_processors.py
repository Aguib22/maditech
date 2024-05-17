from Patients.models import Rendezvous
from Personnel_Service.models import Personnel

def notifications(request):
    if request.user.is_authenticated:
        try:
            personnel = Personnel.objects.get(user=request.user)
            rdv_enAttente = Rendezvous.objects.filter(status_rdv='en attente', personnel=personnel)
            nbr_rdvA = rdv_enAttente.count()
            historique_notif = Rendezvous.objects.filter(personnel=personnel)
        except Personnel.DoesNotExist:
            rdv_enAttente = []
            nbr_rdvA = 0
            historique_notif=[]
            
    else:
        rdv_enAttente = []
        nbr_rdvA = 0
        historique_notif=[]
   

    return {
        'rdv_enAttente': rdv_enAttente,
        'nbr_rdvA': nbr_rdvA,
        'historique_notif':historique_notif
    }