# Generated by Django 4.1.13 on 2024-03-12 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='identifiant',
            field=models.CharField(default='ibrahim224', max_length=30),
            preserve_default=False,
        ),
    ]
