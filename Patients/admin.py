from django.contrib import admin
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Patient,TypeAnalyse,Rendezvous,Examen,Satisfaction,FactureSoins,FactureProduit,DossierMedicaux,Hospitalisation,Consultation

# Register your models here.
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('patient','personnel', 'date_rdv','heure_rdv','status_rdv')
    actions = ['confirmer_reservation','annuler_reservation']

    def confirmer_reservation(self, request, queryset):
        for reservation in queryset:
            reservation.status_rdv = 'confirmé'
            reservation.save()
        """
        subject = 'Confirmation rendez-vous'
            message = "votre rendez-vous a été confirmé"
            from_email = settings.EMAIL_HOST_USER
            to_email = reservation.patient.email
            email = EmailMessage(subject,message,from_email,[to_email])
            email.send()
        """  
        self.message_user(request, "Les rendez-vous sélectionnés ont été confirmés avec succès.")
    confirmer_reservation.short_description = "Confirmer les rendez-vous sélectionnés"
    
    
    def annuler_reservation(self, request, queryset):
        for reservation in queryset:
            reservation.status_rdv = 'annulé'
            reservation.save()
        """
         subject = 'Annulation du rendez-vous'
            message = "Votre rendez-vous a été annulé"
            from_email = settings.EMAIL_HOST_USER
            to_email = reservation.patient.email
            email = EmailMessage(subject, message, from_email, [to_email])
            email.send()
        """
        self.message_user(request, "Les rendez-vous sélectionnés ont été annulés avec succès.")
    annuler_reservation.short_description = "Annuler les rendez-vous sélectionnés"





admin.site.register(Patient)
admin.site.register(Rendezvous, ReservationAdmin)
admin.site.register(TypeAnalyse)
admin.site.register(Examen)
admin.site.register(Satisfaction)
admin.site.register(FactureSoins)
admin.site.register(FactureProduit)
admin.site.register(DossierMedicaux)
admin.site.register(Hospitalisation)
admin.site.register(Consultation)
