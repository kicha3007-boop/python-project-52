from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.users.models import User


class LabelCrudTest(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.client.force_login(User.objects.get(pk=1))

    def test_list(self):
        response = self.client.get(reverse('labels_index'))
        self.assertContains(response, 'feature')

    def test_guest_is_redirected_to_login(self):
        self.client.logout()
        response = self.client.get(reverse('labels_index'))
        self.assertRedirects(response, reverse('login'))

    def test_create(self):
        response = self.client.post(
            reverse('labels_create'), {'name': 'docs'}, follow=True,
        )
        self.assertContains(response, 'Метка успешно создана')
        self.assertTrue(Label.objects.filter(name='docs').exists())

    def test_create_duplicate(self):
        response = self.client.post(reverse('labels_create'), {'name': 'bug'})
        self.assertContains(response, 'уже существует')
        self.assertEqual(Label.objects.filter(name='bug').count(), 1)

    def test_update(self):
        response = self.client.post(
            reverse('labels_update', args=[2]), {'name': 'enhancement'},
            follow=True,
        )
        self.assertContains(response, 'Метка успешно изменена')
        self.assertEqual(Label.objects.get(pk=2).name, 'enhancement')

    def test_delete_unused(self):
        response = self.client.post(
            reverse('labels_delete', args=[2]), follow=True,
        )
        self.assertContains(response, 'Метка успешно удалена')
        self.assertFalse(Label.objects.filter(pk=2).exists())

    def test_delete_used_is_protected(self):
        response = self.client.post(
            reverse('labels_delete', args=[1]), follow=True,
        )
        self.assertContains(response, 'Невозможно удалить метку')
        self.assertTrue(Label.objects.filter(pk=1).exists())
