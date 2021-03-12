"""
    Management app's views.
"""

# - Django modules
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# - Custom models and forms
from .models import Plot, Employee
from .forms import PlotCreationForm, EmployeeCreationForm
from schedule.forms import EventCreationForm
from schedule.models import Event


@staff_member_required
def management_view(request):
    """
    Management main page.

    Gather every needed tool for staff users to manage teams, planning and
    farming plots.

    @staff_member_required

    """
    context = {
        "title": "ALEA: Gestion",
        "plot_form": PlotCreationForm(),
        "emp_form": EmployeeCreationForm(),
        "event_form": EventCreationForm(),
        "employees": Employee.objects.all(),
        "plots": Plot.objects.all(),
        "events": Event.objects.all(),
    }

    return render(request, "management/management.html", context)


@staff_member_required
def add_employee(request):
    """
    Employee adding function

    Add a new employee with connection, data...

    @staff_member_required

    """

    if request.method == "POST":
        form = EmployeeCreationForm(request.POST)

        if form.is_valid():
            form.save()
            request.session["message"] = "Nouvel employé enregistré avec succès !"
            return redirect("management:management")

        else:

            return render(
                request,
                "management/management.html",
                {
                    "form": form,
                },
            )
    else:
        form = EmployeeCreationForm()
        return HttpResponse(status=403)


@staff_member_required
def add_plot(request):
    """
    Plot adding function

    Add a new plot with required data...

    @staff_member_required

    """

    if request.method == "POST":
        form = PlotCreationForm(request.POST)

        if form.is_valid():
            form.save()
            request.session["message"] = "Nouvelle parcelle enregistrée avec succès !"
            return redirect("management:management")

        else:
            return render(
                request,
                "management/management.html",
                {
                    "form": form,
                },
            )
    else:
        return HttpResponse(status=403)


@staff_member_required
def add_event(request):
    """
    Event adding function

    Add a new event to the planning.

    @staff_member_required

    """
    if request.method == "POST":
        form = EventCreationForm(request.POST)

        if form.is_valid():
            event = Event.objects.create(
                employee=form.cleaned_data["employee"],
                plot=form.cleaned_data["plot"],
                day=form.cleaned_data["day"],
                start=form.cleaned_data["start"],
                end=form.cleaned_data["end"],
                occupation=form.cleaned_data["occupation"],
            )
            request.session["message"] = "Nouvel événement enregistrée avec succès !"
            return redirect("management:management")

        else:
            print(form.errors)
            return render(
                request,
                "management/management.html",
                {
                    "form": form,
                },
            )
    else:
        return HttpResponse(status=403)


@staff_member_required
def delete(request, model, id):
    if model == "employee":
        to_delete = Employee.objects.get(pk=id)
        to_delete.delete(keep_parents=False)
        request.session["message"] = "L'employé a été effacé avec succès !"

    if model == "plot":
        to_delete = Plot.objects.get(pk=id)
        to_delete.delete(keep_parents=False)
        request.session["message"] = "La parcelle a été effacée avec succès !"

    if model == "event":
        to_delete = Event.objects.get(pk=id)
        to_delete.delete(keep_parents=False)
        request.session["message"] = "L'événement a été effacé avec succès !"

    return redirect("management:management")
