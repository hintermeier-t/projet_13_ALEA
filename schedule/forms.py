# - Django modules
from django import forms
from django.forms import ModelForm

# - Models
from .models import Event
from management.models import Employee, Plot


class EventCreationForm(ModelForm):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all())

    plot = forms.ModelChoiceField(queryset=Plot.objects.all())
    occupation = forms.CharField(max_length=100, required=True)
    day = forms.ChoiceField(
        choices=(
            ("Lundi", "Lundi"),
            ("Mardi", "Mardi"),
            ("Mercredi", "Mercredi"),
            ("Jeudi", "Jeudi"),
            ("Vendredi", "Vendredi"),
            ("Samedi", "Samedi"),
            ("Dimanche", "Dimanche"),
        )
    )
    start = forms.TimeField()
    end = forms.TimeField()

    class Meta:
        model = Employee
        fields = ("employee", "plot", "day", "start", "end")
