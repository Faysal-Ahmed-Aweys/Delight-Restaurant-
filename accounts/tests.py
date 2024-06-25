from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from reservations.models import Reservation
from datetime import datetime, timedelta
from .forms import UpdateUserForm


class UpdateUserFormTest(TestCase):
    """
    Test cases for the UpdateUserForm form.
    """

    def setUp(self):
        """
        Setup method that creates a test user.
        """
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')

    def test_update_user_form(self):
        """
        Test case to verify updating user details with valid data.
        """
        form_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
        }
        form = UpdateUserForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.username, 'updateduser')
        self.assertEqual(updated_user.email, 'updated@example.com')
        self.assertEqual(updated_user.first_name, 'Updated')
        self.assertEqual(updated_user.last_name, 'User')

    def test_update_user_form_existing_username(self):
        """
        Test case to verify handling of existing username during update.
        """
        User.objects.create_user(username='existinguser', email='existing@example.com', password='password123')
        form_data = {
            'username': 'existinguser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
        }
        form = UpdateUserForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'], ['This username is already taken. Please choose a different one.'])

    def test_update_user_form_existing_email(self):
        """
        Test case to verify handling of existing email during update.
        """
        User.objects.create_user(username='otheruser', email='existing@example.com', password='password123')
        form_data = {
            'username': 'updateduser',
            'email': 'existing@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
        }
        form = UpdateUserForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['This email is already registered. Please choose a different one.'])


class ProfileViewTest(TestCase):
    """
    Test cases for profile-related views.
    """

    def setUp(self):
        """
        Setup method that creates a test user and reservations for testing profile views.
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123', email='test@example.com')
        self.client.login(username='testuser', password='password123')

        # Create some reservations for testing
        self.upcoming_reservation = Reservation.objects.create(
            user=self.user,
            date=datetime.now().date() + timedelta(days=1),
            time=(datetime.now() + timedelta(hours=2)).time(),
            num_people=2,
            status='confirmed'
        )
        self.expired_reservation = Reservation.objects.create(
            user=self.user,
            date=datetime.now().date() - timedelta(days=1),
            time=(datetime.now() - timedelta(hours=2)).time(),
            num_people=2,
            status='completed'
        )

    def test_profile_view(self):
        """
        Test case to verify profile view functionality.
        """
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, 'Upcoming Reservations')
        self.assertContains(response, 'Expired Reservations')

    def test_edit_profile_view(self):
        """
        Test case to verify edit profile view functionality.
        """
        response = self.client.get(reverse('edit_profile', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_details.html')

        # Update user details
        response = self.client.post(reverse('edit_profile', kwargs={'pk': self.user.pk}), {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
        })
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')

    def test_delete_account_confirmation_view(self):
        """
        Test case to verify delete account confirmation view functionality.
        """
        response = self.client.get(reverse('delete_account_confirmation', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_account_confirmation.html')

    def test_delete_account_view(self):
        """
        Test case to verify delete account view functionality.
        """
        response = self.client.post(reverse('delete_account', kwargs={'pk': self.user.pk}), {'action': 'confirm'})
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
