from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# - Models and forms
from .models import Plot, Employee
from .forms import PlotCreationForm, EmployeeCreationForm

@login_required
def management_view(request):
    if request.user.is_staff:
        context = {
            'plot_form': PlotCreationForm(),
            'emp_form': EmployeeCreationForm()
        }

        return render(request, "management/management.html", context)
    else:
        return redirect("dashboard")

@login_required
def add_employee(request):
    if (request.user.is_staff) and (request.method == 'POST'):
        form = EmployeeCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("management/management.html")

        else:
            return render(request, "management/management.html",
                {
                    "form": form,
                })
    else:
        return HttpResponse(status=403)

@login_required
def add_plot(request):
    if (request.user.is_staff) and (request.method == 'POST'):
        form = PlotCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("management/management.html")

        else:
            return render(request, "management/management.html",
                {
                    "form": form,
                })
    else:
        return HttpResponse(status=403)