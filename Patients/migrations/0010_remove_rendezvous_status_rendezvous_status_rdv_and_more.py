# Generated by Django 4.1.1 on 2024-04-08 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patients', '0009_alter_rendezvous_patient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rendezvous',
            name='status',
        ),
        migrations.AddField(
            model_name='rendezvous',
            name='status_rdv',
            field=models.CharField(choices=[('confirmé', 'confirmé'), ('en attente', 'en attente'), ('annulé', 'annulé')], default='en attente', max_length=32),
        ),
        migrations.AlterField(
            model_name='rendezvous',
            name='sujet_rdv',
            field=models.TextField(blank=True, null=True),
        ),
    ]
