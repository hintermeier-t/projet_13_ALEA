from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

class Plot(models.Model):
    variety = models.CharField("Variété", max_length=50, null=False)
    area = models.CharField("Etendue",max_length=20, null=False)
    comment = models.CharField("Commentaire", max_length=500, null=True)
    plowed = models.BooleanField("Labourée")
    watered = models.BooleanField("Arrosée")
    sulphated = models.BooleanField("Traitée")
    class Meta:
        verbose_name = "Parcelle"

class Employee(User):
    phone_number = models.CharField("Téléphone", max_length=10)
    address = models.CharField("Adresse", max_length=200)

    class Meta:
        verbose_name = "Employé"