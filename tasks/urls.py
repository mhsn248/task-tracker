from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register', ),

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

    path(
        '<int:task_id>/edit/',
        views.task_update,
        name='task_update',
    ),

    path(
        '<int:task_id>/delete/',
        views.task_delete,
        name='task_delete',
    ),

    path(
        '<int:task_id>/deactivate/',
        views.task_deactivate,
        name='task_deactivate',
    ),
]
