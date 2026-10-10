from django.conf import settings
from django.db import models

from task_manager.labels.models import Label
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField('Имя', max_length=150, unique=True)
    description = models.TextField('Описание', blank=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='tasks',
        verbose_name='Статус',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='authored_tasks',
        verbose_name='Автор',
    )
    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='executed_tasks',
        null=True,
        blank=True,
        verbose_name='Исполнитель',
    )
    labels = models.ManyToManyField(
        Label,
        through='TaskLabel',
        related_name='tasks',
        blank=True,
        verbose_name='Метки',
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.name


class TaskLabel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('task', 'label')
