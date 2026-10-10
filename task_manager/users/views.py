from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.mixins import OwnerRequiredMixin, ProtectedDeleteMixin
from task_manager.users.forms import UserForm
from task_manager.users.models import User


class UserOwnerMixin(OwnerRequiredMixin):
    model = User
    permission_message = 'У вас нет прав для изменения другого пользователя.'
    permission_redirect_url = reverse_lazy('users_index')
    success_url = reverse_lazy('users_index')


class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'
    ordering = ['id']


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserForm
    template_name = 'form.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'
    extra_context = {'title': 'Регистрация', 'button_text': 'Зарегистрировать'}


class UserUpdateView(UserOwnerMixin, SuccessMessageMixin, UpdateView):
    form_class = UserForm
    template_name = 'form.html'
    success_message = 'Пользователь успешно изменен'
    extra_context = {
        'title': 'Изменение пользователя',
        'button_text': 'Изменить',
    }


class UserDeleteView(
    UserOwnerMixin, ProtectedDeleteMixin, SuccessMessageMixin, DeleteView
):
    template_name = 'delete.html'
    success_message = 'Пользователь успешно удален'
    protected_message = (
        'Невозможно удалить пользователя, потому что он используется'
    )
    protected_redirect_url = reverse_lazy('users_index')
    extra_context = {'title': 'Удаление пользователя'}
