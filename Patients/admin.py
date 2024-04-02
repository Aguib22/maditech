from django.contrib import admin
from .models import Patient,TypeAnalyse,Rendezvous,Examen,Satisfaction,FactureSoins,FactureProduit,DossierMedicaux,Hospitalisation,Consultation

# Register your models here.
admin.site.register(Patient)
admin.site.register(Rendezvous)
admin.site.register(TypeAnalyse)
admin.site.register(Examen)
admin.site.register(Satisfaction)
admin.site.register(FactureSoins)
admin.site.register(FactureProduit)
admin.site.register(DossierMedicaux)
admin.site.register(Hospitalisation)
admin.site.register(Consultation)
