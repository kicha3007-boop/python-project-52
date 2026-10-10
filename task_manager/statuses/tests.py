from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.users.models import User


class StatusCrudTest(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.client.force_login(User.objects.get(pk=1))

    def test_list(self):
        response = self.client.get(reverse('statuses_index'))
        self.assertContains(response, 'в работе')

    def test_guest_is_redirected_to_login(self):
        self.client.logout()
        response = self.client.get(reverse('statuses_index'))
        self.assertRedirects(response, reverse('login'))

    def test_create(self):
        response = self.client.post(
            reverse('statuses_create'), {'name': 'на тестировании'},
            follow=True,
        )
        self.assertContains(response, 'Статус успешно создан')
        self.assertTrue(Status.objects.filter(name='на тестировании').exists())

    def test_create_duplicate(self):
        response = self.client.post(
            reverse('statuses_create'), {'name': 'новый'},
        )
        self.assertContains(response, 'уже существует')
        self.assertEqual(Status.objects.filter(name='новый').count(), 1)

    def test_create_empty(self):
        response = self.client.post(reverse('statuses_create'), {'name': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.count(), 2)

    def test_update(self):
        response = self.client.post(
            reverse('statuses_update', args=[2]), {'name': 'завершен'},
            follow=True,
        )
        self.assertContains(response, 'Статус успешно изменен')
        self.assertEqual(Status.objects.get(pk=2).name, 'завершен')

    def test_delete_unused(self):
        unused = Status.objects.create(name='архив')
        response = self.client.post(
            reverse('statuses_delete', args=[unused.pk]), follow=True,
        )
        self.assertContains(response, 'Статус успешно удален')
        self.assertFalse(Status.objects.filter(pk=unused.pk).exists())

    def test_delete_used_is_protected(self):
        response = self.client.post(
            reverse('statuses_delete', args=[1]), follow=True,
        )
        self.assertContains(response, 'Невозможно удалить статус')
        self.assertTrue(Status.objects.filter(pk=1).exists())
