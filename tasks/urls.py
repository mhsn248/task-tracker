from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),

    path(
        'create/',
        views.task_create,
        name='task_create',
    ),

    path(
        'daily/',
        views.daily_tasks,
        name='daily_tasks',
    ),

    path(
        'teacher/students/',
        views.teacher_students,
        name='teacher_students',
    ),

    path(
        'teacher/students/<int:student_id>/',
        views.teacher_student_detail,
        name='teacher_student_detail',
    ),
]
