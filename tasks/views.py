from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Task


@login_required
def task_list(request):

    tasks = Task.objects.filter(
        student=request.user,
        is_active=True,
    )

    context = {
        'tasks': tasks,
    }

    return render(
        request,
        'tasks/task_list.html',
        context,
    )
