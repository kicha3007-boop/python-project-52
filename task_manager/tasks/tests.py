from django.test import TestCase
from django.urls import reverse

from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskCrudTest(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.author = User.objects.get(pk=1)
        self.client.force_login(self.author)
        self.form_data = {
            'name': 'Write docs',
            'description': 'README',
            'status': 1,
            'executor': 2,
            'labels': [1, 2],
        }

    def test_guest_is_redirected_to_login(self):
        self.client.logout()
        response = self.client.get(reverse('tasks_index'))
        self.assertRedirects(response, reverse('login'))

    def test_list(self):
        response = self.client.get(reverse('tasks_index'))
        self.assertContains(response, 'Fix login')
        self.assertContains(response, 'Add filter')

    def test_show(self):
        response = self.client.get(reverse('tasks_show', args=[1]))
        self.assertContains(response, 'Login form fails')
        self.assertContains(response, 'Anna Smith')
        self.assertContains(response, 'bug')

    def test_create_sets_author(self):
        response = self.client.post(
            reverse('tasks_create'), self.form_data, follow=True,
        )
        self.assertContains(response, 'Задача успешно создана')
        task = Task.objects.get(name='Write docs')
        self.assertEqual(task.author, self.author)
        self.assertEqual(task.labels.count(), 2)

    def test_create_duplicate(self):
        self.form_data['name'] = 'Fix login'
        response = self.client.post(reverse('tasks_create'), self.form_data)
        self.assertContains(response, 'уже существует')

    def test_update(self):
        response = self.client.post(
            reverse('tasks_update', args=[2]), self.form_data, follow=True,
        )
        self.assertContains(response, 'Задача успешно изменена')
        task = Task.objects.get(pk=2)
        self.assertEqual(task.name, 'Write docs')
        self.assertEqual(task.author.pk, 2)

    def test_delete_by_author(self):
        response = self.client.post(
            reverse('tasks_delete', args=[1]), follow=True,
        )
        self.assertContains(response, 'Задача успешно удалена')
        self.assertFalse(Task.objects.filter(pk=1).exists())

    def test_delete_by_other_user_is_forbidden(self):
        response = self.client.post(
            reverse('tasks_delete', args=[2]), follow=True,
        )
        self.assertContains(response, 'Задачу может удалить только ее автор')
        self.assertTrue(Task.objects.filter(pk=2).exists())


class TaskFilterTest(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.client.force_login(User.objects.get(pk=1))

    def get_task_names(self, params):
        response = self.client.get(reverse('tasks_index'), params)
        return {task.name for task in response.context['tasks']}

    def test_filter_by_status(self):
        self.assertEqual(self.get_task_names({'status': 2}), {'Add filter'})

    def test_filter_by_executor(self):
        self.assertEqual(self.get_task_names({'executor': 2}), {'Fix login'})

    def test_filter_by_label(self):
        self.assertEqual(self.get_task_names({'label': 1}), {'Fix login'})

    def test_filter_self_tasks(self):
        names = self.get_task_names({'self_tasks': 'on'})
        self.assertEqual(names, {'Fix login'})

    def test_no_filters(self):
        names = self.get_task_names({})
        self.assertEqual(names, {'Fix login', 'Add filter'})
