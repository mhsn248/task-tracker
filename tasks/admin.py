from django.contrib import admin
from .models import Task, DailyTaskStatus


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'student',
        'is_active',
        'created_at',
    )

    list_filter = (
        'is_active',
    )

    search_fields = (
        'title',
        'student__username',
    )


@admin.register(DailyTaskStatus)
class DailyTaskStatusAdmin(admin.ModelAdmin):

    list_display = (
        'task',
        'date',
        'is_completed',
    )

    list_filter = (
        'date',
        'is_completed',
    )

    search_fields = (
        'task__title',
        'task__student__username',
    )
