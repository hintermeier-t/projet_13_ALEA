from django.db import models
from management.models import Employee

# Create your models here.
class Message (models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=500)
    date = models.DateTimeField()