from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class HomeViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_view_as_staff(self):
        """
        Test home view for staff user.
        """
        # Create a staff user
        staff_user = User.objects.create_user(username='staffuser', password='password123', is_staff=True)
        self.client.force_login(staff_user)

        # Make a GET request to the home view
        response = self.client.get(reverse('home'))

        # Check if it redirects to staff dashboard
        self.assertRedirects(response, reverse('staff_dashboard'))

    def test_home_view_as_non_staff(self):
        """
        Test home view for non-staff user.
        """
        # Create a regular user
        regular_user = User.objects.create_user(username='regularuser', password='password123', is_staff=False)
        self.client.force_login(regular_user)

        # Make a GET request to the home view
        response = self.client.get(reverse('home'))

        # Check if it renders index.html template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
