from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TaskForm
from datetime import date
from .models import DailyTaskStatus

from .models import Task


@login_required
def task_list(request):

    tasks = Task.objects.filter(
        student=request.user,
        is_active=True,
    ).order_by('display_order')

    context = {
        'tasks': tasks,
    }

    return render(
        request,
        'tasks/task_list.html',
        context,
    )


@login_required
def task_create(request):

    if request.method == 'POST':

        form = TaskForm(request.POST)

        if form.is_valid():

            task = form.save(commit=False)

            task.student = request.user

            task.save()

            return redirect('task_list')

    else:

        form = TaskForm()

    return render(
        request,
        'tasks/task_form.html',
        {
            'form': form,
        },
    )


@login_required
def today_tasks(request):

    today = date.today()

    tasks = Task.objects.filter(
        student=request.user,
        is_active=True,
    ).order_by('display_order')

    if request.method == 'POST':

        for task in tasks:

            is_completed = (
                f'task_{task.id}' in request.POST
            )

            DailyTaskStatus.objects.update_or_create(
                task=task,
                date=today,
                defaults={
                    'is_completed': is_completed,
                }
            )

        return redirect('today_tasks')

    statuses = {
        status.task_id: status.is_completed
        for status in DailyTaskStatus.objects.filter(
            task__in=tasks,
            date=today,
        )
    }

    context = {
        'tasks': tasks,
        'statuses': statuses,
        'today': today,
    }

    return render(
        request,
        'tasks/today_tasks.html',
        context,
    )
