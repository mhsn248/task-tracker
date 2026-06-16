from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TaskForm, RegisterForm
from datetime import date
from .models import DailyTaskStatus
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from datetime import date, datetime
from django.db.models import Q
from .models import Task
from django.contrib.auth import login
from django.contrib.auth.models import Group


@login_required
def task_list(request):

    tasks = Task.objects.filter(
        student=request.user,
        deactivated_at__isnull=True,
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
def daily_tasks(request):

    selected_date = request.GET.get('date')

    if selected_date:

        try:
            selected_date = datetime.strptime(
                selected_date,
                '%Y-%m-%d'
            ).date()

        except ValueError:

            selected_date = date.today()

    else:

        selected_date = date.today()

    tasks = Task.objects.filter(
        student=request.user,
    ).filter(
        Q(started_at__lte=selected_date)
        &
        (
            Q(deactivated_at__isnull=True)
            |
            Q(deactivated_at__gt=selected_date)
        )
    ).order_by(
        'display_order',
    )

    if request.method == 'POST':

        for task in tasks:

            is_completed = (
                f'task_{task.id}' in request.POST
            )

            DailyTaskStatus.objects.update_or_create(
                task=task,
                date=selected_date,
                defaults={
                    'is_completed': is_completed,
                }
            )

        return redirect(
            f'/tasks/daily/?date={selected_date}'
        )

    statuses = {
        status.task_id: status.is_completed
        for status in DailyTaskStatus.objects.filter(
            task__in=tasks,
            date=selected_date,
        )
    }

    context = {
        'tasks': tasks,
        'statuses': statuses,
        'selected_date': selected_date,
    }

    return render(
        request,
        'tasks/daily_tasks.html',
        context,
    )


@login_required
def teacher_students(request):

    if not request.user.groups.filter(
        name='Teacher'
    ).exists():

        return redirect('task_list')

    students = User.objects.filter(
        groups__name='Student'
    ).order_by('username')

    context = {
        'students': students,
    }

    return render(
        request,
        'tasks/teacher_students.html',
        context,
    )


@login_required
def teacher_student_detail(
    request,
    student_id,
):

    if not request.user.groups.filter(
        name='Teacher'
    ).exists():

        return redirect('task_list')

    student = get_object_or_404(
        User,
        id=student_id,
        groups__name='Student',
    )

    selected_date = request.GET.get('date')

    if selected_date:

        try:

            selected_date = datetime.strptime(
                selected_date,
                '%Y-%m-%d',
            ).date()

        except ValueError:

            selected_date = date.today()

    else:

        selected_date = date.today()

    tasks = Task.objects.filter(
        student=student,
    ).filter(
        Q(started_at__lte=selected_date)
        &
        (
            Q(deactivated_at__isnull=True)
            |
            Q(deactivated_at__gt=selected_date)
        )
    ).order_by(
        'display_order',
    )

    statuses = {
        status.task_id: status.is_completed
        for status in DailyTaskStatus.objects.filter(
            task__in=tasks,
            date=selected_date,
        )
    }

    context = {
        'student': student,
        'tasks': tasks,
        'statuses': statuses,
        'selected_date': selected_date,
    }

    return render(
        request,
        'tasks/teacher_student_detail.html',
        context,
    )


@login_required
def task_update(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        student=request.user,
    )

    if request.method == 'POST':

        form = TaskForm(
            request.POST,
            instance=task,
        )

        if form.is_valid():

            form.save()

            return redirect('task_list')

    else:

        form = TaskForm(
            instance=task,
        )

    return render(
        request,
        'tasks/task_form.html',
        {
            'form': form,
            'page_title': 'ویرایش کار',
        },
    )


@login_required
def task_delete(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        student=request.user,
    )

    if request.method == 'POST':

        task.delete()

        return redirect('task_list')

    return render(
        request,
        'tasks/task_confirm_delete.html',
        {
            'task': task,
        },
    )


@login_required
def task_deactivate(request, task_id):

    task = get_object_or_404(
        Task,
        id=task_id,
        student=request.user,
    )

    if request.method == 'POST':

        task.deactivated_at = date.today()

        task.save()

        return redirect('task_list')

    return render(
        request,
        'tasks/task_confirm_deactivate.html',
        {
            'task': task,
        },
    )


def register(request):

    if request.user.is_authenticated:

        return redirect('daily_tasks')

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            student_group, _ = Group.objects.get_or_create(
                name='Student'
            )

            user.groups.add(student_group)

            login(request, user)

            return redirect('daily_tasks')

    else:

        form = RegisterForm()

    return render(

        request,

        'registration/register.html',

        {

            'form': form,

        },

    )
