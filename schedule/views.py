"""
    Schedule app's views.
"""

# - Django modules
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# - Custom modules and models
from .models import Event
from management.models import Employee

@login_required
def display_planning(request):

    event_list= Event.objects.filter(
        employee_id = Employee.objects.get(
            user_ptr_id = request.user.id
        )
    ).order_by('day', 'start')
    context = {
        'events' : event_list,
        'title' : 'ALEA: Mon Planning'
    }

    return render(request, "schedule/planning.html", context)
    
