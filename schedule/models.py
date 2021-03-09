from django.db import models
from management.models import Plot, Employee

# Create your models here.
class Event(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=False)
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE, null=False)
    day = models.CharField(max_length=10)
    start = models.TimeField()
    end = models.TimeField()
    occupation = models.CharField(max_length=100, null=False)
