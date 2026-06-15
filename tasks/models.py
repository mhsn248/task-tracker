from django.db import models
from django.contrib.auth.models import User


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

    class Meta:
        ordering = ['title']
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'title'],
                name='unique_task_per_student',
            )
        ]

    def __str__(self):
        return f'{self.student.username} - {self.title}'
