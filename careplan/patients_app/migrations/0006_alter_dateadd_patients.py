# Generated by Django 4.2.1 on 2023-05-29 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patients_app', '0005_alter_medicalcomponent_patients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dateadd',
            name='patients',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='date_add', to='patients_app.patients'),
        ),
    ]
