from django.db import models
from django.contrib.auth.models import User, AbstractUser


class Plot(models.Model):
    variety = models.CharField("Variété", max_length=50, null=False)
    area = models.CharField("Etendue", max_length=20, null=False)
    comment = models.CharField("Commentaire", max_length=500, blank=True)
    plowed = models.BooleanField("Labourée")
    watered = models.BooleanField("Arrosée")
    sulphated = models.BooleanField("Traitée")

    def __str__(self):
        return "No. " + str(self.id) + " : " + self.variety

    class Meta:
        verbose_name = "Parcelle"


class Employee(User):
    phone_number = models.CharField("Téléphone", max_length=10)
    address = models.CharField("Adresse", max_length=200)

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = "Employé"
