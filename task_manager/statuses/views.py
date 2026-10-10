from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import AuthRequiredMixin, ProtectedDeleteMixin
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class StatusMixin(AuthRequiredMixin, SuccessMessageMixin):
    model = Status
    success_url = reverse_lazy('statuses_index')


class StatusListView(AuthRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'
    ordering = ['id']


class StatusCreateView(StatusMixin, CreateView):
    form_class = StatusForm
    template_name = 'form.html'
    success_message = 'Статус успешно создан'
    extra_context = {'title': 'Создать статус', 'button_text': 'Создать'}


class StatusUpdateView(StatusMixin, UpdateView):
    form_class = StatusForm
    template_name = 'form.html'
    success_message = 'Статус успешно изменен'
    extra_context = {'title': 'Изменение статуса', 'button_text': 'Изменить'}


class StatusDeleteView(StatusMixin, ProtectedDeleteMixin, DeleteView):
    template_name = 'delete.html'
    success_message = 'Статус успешно удален'
    protected_message = 'Невозможно удалить статус'
    protected_redirect_url = reverse_lazy('statuses_index')
    extra_context = {'title': 'Удаление статуса'}
