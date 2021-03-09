# - Django Modules
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm

# - Models
from .models import Plot, Employee

class PlotCreationForm(ModelForm):
    
    class Meta:

        model = Plot
        fields = [
            'variety', 'area', 'comment', 'plowed', 'watered', 'sulphated'
            ]

class EmployeeCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Employee
        fields =(
            UserCreationForm.Meta.fields
            + ('first_name','last_name','email', 'phone_number','address')
            )