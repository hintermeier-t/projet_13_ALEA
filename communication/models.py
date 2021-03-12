"""
        Communication app's view
"""

# - Django Modules
from django.db import models
from management.models import Employee


class Message(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=500)
    date = models.DateTimeField()
