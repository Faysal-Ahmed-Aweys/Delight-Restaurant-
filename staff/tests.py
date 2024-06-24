from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages

class StaffDashboardViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(username='staffuser', password='12345', is_staff=True)
        self.non_staff_user = User.objects.create_user(username='nonstaffuser', password='12345', is_staff=False)

    def test_staff_user_can_access_dashboard(self):
        self.client.login(username='staffuser', password='12345')
        response = self.client.get(reverse('staff_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff_dashboard.html')

    def test_non_staff_user_redirected(self):
        self.client.login(username='nonstaffuser', password='12345')
        response = self.client.get(reverse('staff_dashboard'))
        self.assertEqual(response.status_code, 302)  # Should redirect to home
        self.assertRedirects(response, reverse('home'))

        # Verify message is added
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You are not authorized to view this page')
