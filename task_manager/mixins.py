from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect


class AuthRequiredMixin(LoginRequiredMixin):
    login_message = 'Вы не авторизованы! Пожалуйста, выполните вход.'

    def handle_no_permission(self):
        messages.error(self.request, self.login_message)
        return redirect('login')


class OwnerRequiredMixin(AuthRequiredMixin):
    """Доступ к объекту только у его владельца: get_owner() задаёт кого."""

    permission_message = ''
    permission_redirect_url = ''

    def get_owner(self, obj):
        return obj

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.get_owner(self.get_object()) != request.user:
            messages.error(request, self.permission_message)
            return redirect(self.permission_redirect_url)
        return super().dispatch(request, *args, **kwargs)


class ProtectedDeleteMixin:
    """Удаление, которое запрещает внешний ключ с on_delete=PROTECT."""

    protected_message = ''
    protected_redirect_url = ''

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_redirect_url)
