import django_filters
from django import forms

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    label = django_filters.ModelChoiceFilter(
        field_name='labels',
        queryset=Label.objects.all(),
        label='Метка',
    )
    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks',
        widget=forms.CheckboxInput,
        label='Только свои задачи',
    )

    class Meta:
        model = Task
        fields = ('status', 'executor', 'label', 'self_tasks')

    def filter_self_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
