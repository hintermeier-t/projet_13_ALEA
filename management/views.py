"""
    Management app's views.
"""

# - Django modules
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# - Custom models and forms
from schedule.forms import EventCreationForm
from .forms import PlotCreationForm, EmployeeCreationForm
from schedule.models import Event


@login_required
def management_view(request):
    """
    Management main page.

    Gather every needed tool for staff users to manage teams, planning and
    farming plots.

    @login_required
    user.is_staff ONLY

    """
    if request.user.is_staff:
        context = {
            "plot_form": PlotCreationForm(),
            "emp_form": EmployeeCreationForm(),
            "event_form": EventCreationForm(),
        }

        return render(request, "management/management.html", context)
    else:
        return redirect("dashboard")


@login_required
def add_employee(request):
    """
    Employee adding function

    Add a new employee with connection, data...

    @login_required
    user.is_staff ONLY
    
    """
    if (request.user.is_staff) and (request.method == "POST"):
        form = EmployeeCreationForm(request.POST)

        if form.is_valid():
            form.save()
            request.session["message"] = (
                "Nouvel employé enregistré avec succès !"
                )
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


@login_required
def add_plot(request):
    """
    Plot adding function

    Add a new plot with required data...

    @login_required
    user.is_staff ONLY
    
    """
    if (request.user.is_staff) and (request.method == "POST"):
        form = PlotCreationForm(request.POST)

        if form.is_valid():
            form.save()
            request.session["message"] = (
                "Nouvelle parcelle enregistrée avec succès !"
                )
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


@login_required
def add_event(request):
    """
    Event adding function

    Add a new event to the planning.

    @login_required
    user.is_staff ONLY
    
    """
    if (request.user.is_staff) and (request.method == "POST"):
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
            request.session["message"] = (
                "Nouvel événement enregistrée avec succès !"
                )
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
