from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from task_manager.mixins import AuthRequiredMixin, OwnerRequiredMixin
from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.forms import TaskForm
from task_manager.tasks.models import Task


class TaskMixin(SuccessMessageMixin):
    model = Task
    success_url = reverse_lazy('tasks_index')


class TaskListView(AuthRequiredMixin, FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return (
            Task.objects
            .select_related('status', 'author', 'executor')
            .order_by('id')
        )


class TaskDetailView(AuthRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/show.html'
    context_object_name = 'task'


class TaskCreateView(AuthRequiredMixin, TaskMixin, CreateView):
    form_class = TaskForm
    template_name = 'form.html'
    success_message = 'Задача успешно создана'
    extra_context = {'title': 'Создать задачу', 'button_text': 'Создать'}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(AuthRequiredMixin, TaskMixin, UpdateView):
    form_class = TaskForm
    template_name = 'form.html'
    success_message = 'Задача успешно изменена'
    extra_context = {'title': 'Изменение задачи', 'button_text': 'Изменить'}


class TaskDeleteView(OwnerRequiredMixin, TaskMixin, DeleteView):
    template_name = 'delete.html'
    success_message = 'Задача успешно удалена'
    permission_message = 'Задачу может удалить только ее автор'
    permission_redirect_url = reverse_lazy('tasks_index')
    extra_context = {'title': 'Удаление задачи'}

    def get_owner(self, obj):
        return obj.author
