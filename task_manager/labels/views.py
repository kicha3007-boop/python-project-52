from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.mixins import AuthRequiredMixin, ProtectedDeleteMixin


class LabelMixin(AuthRequiredMixin, SuccessMessageMixin):
    model = Label
    success_url = reverse_lazy('labels_index')


class LabelListView(AuthRequiredMixin, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'
    ordering = ['id']


class LabelCreateView(LabelMixin, CreateView):
    form_class = LabelForm
    template_name = 'form.html'
    success_message = 'Метка успешно создана'
    extra_context = {'title': 'Создать метку', 'button_text': 'Создать'}


class LabelUpdateView(LabelMixin, UpdateView):
    form_class = LabelForm
    template_name = 'form.html'
    success_message = 'Метка успешно изменена'
    extra_context = {'title': 'Изменение метки', 'button_text': 'Изменить'}


class LabelDeleteView(LabelMixin, ProtectedDeleteMixin, DeleteView):
    template_name = 'delete.html'
    success_message = 'Метка успешно удалена'
    protected_message = 'Невозможно удалить метку'
    protected_redirect_url = reverse_lazy('labels_index')
    extra_context = {'title': 'Удаление метки'}
