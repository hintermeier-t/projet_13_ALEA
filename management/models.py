from django.db import models

# Create your models here.

class Plot(models.Model):
    variety = models.CharField(max_length=50, null=False)
    area = models.CharField(max_length=20, null=False)
    comment = models.CharField(max_length=500, null=True)
    plowed = models.BooleanField()
    watered = models.BooleanField()
    sulphated = models.BooleanField()
    class Meta:
        verbose_name = "Parcelle"