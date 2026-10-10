from django.test import TestCase
from django.urls import reverse

from task_manager.users.models import User


class UserCrudTest(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.other = User.objects.get(pk=2)
        self.form_data = {
            'first_name': 'Ivan',
            'last_name': 'Petrov',
            'username': 'ipetrov',
            'password1': 'secret123',
            'password2': 'secret123',
        }

    def test_list_is_public(self):
        response = self.client.get(reverse('users_index'))
        self.assertContains(response, 'jdoe')
        self.assertContains(response, 'Anna Smith')

    def test_register(self):
        response = self.client.post(reverse('users_create'), self.form_data)
        self.assertRedirects(response, reverse('login'))
        user = User.objects.get(username='ipetrov')
        self.assertTrue(user.check_password('secret123'))

    def test_register_duplicate_username(self):
        self.form_data['username'] = 'jdoe'
        response = self.client.post(reverse('users_create'), self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'уже существует')

    def test_login_and_logout(self):
        self.user.set_password('secret123')
        self.user.save()
        response = self.client.post(
            reverse('login'),
            {'username': 'jdoe', 'password': 'secret123'},
            follow=True,
        )
        self.assertRedirects(response, reverse('index'))
        self.assertContains(response, 'Вы залогинены')

        response = self.client.post(reverse('logout'), follow=True)
        self.assertContains(response, 'Вы разлогинены')

    def test_update_self(self):
        self.client.force_login(self.user)
        self.form_data['username'] = 'jdoe'
        response = self.client.post(
            reverse('users_update', args=[self.user.pk]), self.form_data,
        )
        self.assertRedirects(response, reverse('users_index'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Ivan')

    def test_update_other_is_forbidden(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users_update', args=[self.other.pk]),
            self.form_data,
            follow=True,
        )
        self.assertContains(response, 'У вас нет прав для изменения')
        self.other.refresh_from_db()
        self.assertEqual(self.other.first_name, 'Anna')

    def test_update_by_guest_redirects_to_login(self):
        response = self.client.get(
            reverse('users_update', args=[self.user.pk]),
        )
        self.assertRedirects(response, reverse('login'))

    def test_delete_user_without_tasks(self):
        free_user = User.objects.create_user('free', password='secret123')
        self.client.force_login(free_user)
        response = self.client.post(
            reverse('users_delete', args=[free_user.pk]), follow=True,
        )
        self.assertContains(response, 'Пользователь успешно удален')
        self.assertFalse(User.objects.filter(pk=free_user.pk).exists())

    def test_delete_user_with_tasks_is_protected(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users_delete', args=[self.user.pk]), follow=True,
        )
        self.assertContains(response, 'Невозможно удалить пользователя')
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())
