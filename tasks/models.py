from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
    )

    title = models.CharField(
        max_length=255,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    display_order = models.PositiveIntegerField(
        default=0,
    )

    class Meta:
        ordering = ['display_order', 'title']

        constraints = [
            models.UniqueConstraint(
                fields=['student', 'title'],
                name='unique_task_per_student',
            )
        ]

    def save(self, *args, **kwargs):

        # فقط هنگام ایجاد Task جدید
        if self.pk is None:

            # اگر ترتیب مشخص نشده باشد
            if self.display_order <= 0:

                last_task = Task.objects.filter(
                    student=self.student,
                    is_active=True,
                ).order_by('-display_order').first()

                if last_task:
                    self.display_order = (
                        last_task.display_order + 1
                    )
                else:
                    self.display_order = 1

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f'{self.student.username} - '
            f'{self.display_order}. {self.title}'
        )


class DailyTaskStatus(models.Model):

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='daily_statuses',
    )

    date = models.DateField()

    is_completed = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:

        ordering = ['-date', 'task__display_order']

        constraints = [
            models.UniqueConstraint(
                fields=['task', 'date'],
                name='unique_task_per_day',
            )
        ]

    def __str__(self):

        status = '✓' if self.is_completed else '✗'

        return (
            f'{self.task.student.username} - '
            f'{self.task.title} - '
            f'{self.date} - '
            f'{status}'
        )
