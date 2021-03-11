"""
    Communication app's views.
"""
# - Built-in module
from datetime import datetime

# - Django modules
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# - Custom models
from .models import Message
from management.models import Employee

@login_required
def chat (request):
    if request.method == 'POST':
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        content = request.POST['content']
        Message.objects.create(
            employee = Employee.objects.get(
                user_ptr_id = request.user.id
            ),
            content = content,
            date = date
        )

    messages = Message.objects.all().order_by("date")
    context = {
        'title' : 'ALEA: Messagerie',
        "messages" : messages,
    }
    return render(request, 'communication/chat.html', context)