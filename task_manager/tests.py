from django.test import TestCase
from django.urls import reverse


class IndexTest(TestCase):
    def test_guest_menu(self):
        response = self.client.get(reverse('index'))
        for text in ('Менеджер задач', 'Пользователи', 'Вход', 'Регистрация'):
            self.assertContains(response, text)
