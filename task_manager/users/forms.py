from django.contrib.auth.forms import UserCreationForm

from task_manager.users.models import User


class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username')

    def clean_username(self):
        # При правке своя же запись не должна считаться дубликатом
        username = self.cleaned_data.get('username')
        duplicates = User.objects.filter(username__iexact=username)
        if self.instance.pk:
            duplicates = duplicates.exclude(pk=self.instance.pk)
        if username and duplicates.exists():
            self.add_error(
                'username',
                self.instance.unique_error_message(User, ['username']),
            )
        return username
