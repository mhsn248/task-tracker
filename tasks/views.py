from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import TaskForm

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
