from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import date, time, timedelta
from .models import Reservation
from .forms import ReservationForm, EditReservationForm
from .views import reserve, edit_reservation

class ReservationModelTest(TestCase):
    """Test case for Reservation model."""
    
    def setUp(self):
        """Set up initial data for tests."""
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.reservation = Reservation.objects.create(
            user=self.user,
            date=timezone.now().date() + timedelta(days=1),
            time=time(12, 0),
            num_people=4,
            status='approved'
        )

    def test_reservation_creation(self):
        """Test the creation of a reservation."""
        self.assertEqual(self.reservation.user.username, 'testuser')
        self.assertEqual(self.reservation.date, timezone.now().date() + timedelta(days=1))
        self.assertEqual(self.reservation.time, time(12, 0))
        self.assertEqual(self.reservation.num_people, 4)
        self.assertEqual(self.reservation.status, 'approved')

    def test_unique_together_constraint(self):
        """Test the unique constraint for date, time, and user."""
        with self.assertRaises(Exception):
            Reservation.objects.create(
                user=self.user,
                date=timezone.now().date() + timedelta(days=1),
                time=time(12, 0),
                num_people=2,
                status='approved'
            )

class ReservationFormTest(TestCase):
    """Test case for ReservationForm."""
    
    def setUp(self):
        """Set up initial data for tests."""
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_reservation_form_valid(self):
        """Test the reservation form with valid data."""
        form_data = {
            'date': timezone.now().date() + timedelta(days=1),
            'time': '12:00',
            'num_people': 4,
        }
        form = ReservationForm(data=form_data)
        self.assertTrue(form.is_valid())

class EditReservationFormTest(TestCase):
    """Test case for EditReservationForm."""
    
    def setUp(self):
        """Set up initial data for tests."""
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.reservation = Reservation.objects.create(
            user=self.user,
            date=timezone.now().date() + timedelta(days=1),
            time=time(12, 0),
            num_people=4,
            status='approved'
        )

    def test_edit_reservation_form_valid(self):
        """Test the edit reservation form with valid data."""
        form_data = {
            'date': timezone.now().date() + timedelta(days=1),
            'time': '14:00',
            'num_people': 3,
        }
        form = EditReservationForm(data=form_data, instance=self.reservation)
        self.assertTrue(form.is_valid())
        

class ReservationViewsTest(TestCase):
    """Test case for reservation-related views."""
    
    def setUp(self):
        """Set up initial data for tests."""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_reserve_view_get(self):
        """Test the GET request to the reserve view."""
        request = self.factory.get(reverse('reserve'))
        request.user = self.user
        response = reserve(request)
        self.assertEqual(response.status_code, 200)

    def test_reserve_view_post_valid(self):
        """Test the POST request to the reserve view with valid data."""
        request = self.factory.post(reverse('reserve'), {
            'date': timezone.now().date() + timedelta(days=1),
            'time': '14:00',
            'num_people': 3,
        })
        request.user = self.user
        response = reserve(request)
        self.assertEqual(response.status_code, 302)  # Redirects upon successful reservation


    def test_edit_reservation_view_get(self):
        """Test the GET request to the edit reservation view."""
        reservation = Reservation.objects.create(
            user=self.user,
            date=timezone.now().date() + timedelta(days=1),
            time=time(12, 0),
            num_people=4,
            status='approved'
        )
        request = self.factory.get(reverse('edit_reservation', args=[reservation.pk]))
        request.user = self.user
        response = edit_reservation(request, pk=reservation.pk)
        self.assertEqual(response.status_code, 200)

    def test_edit_reservation_view_post_valid(self):
        """Test the POST request to the edit reservation view with valid data."""
        reservation = Reservation.objects.create(
            user=self.user,
            date=timezone.now().date() + timedelta(days=1),
            time=time(12, 0),
            num_people=4,
            status='approved'
        )
        request = self.factory.post(reverse('edit_reservation', args=[reservation.pk]), {
            'date': timezone.now().date() + timedelta(days=1),
            'time': '14:00',
            'num_people': 3,
        })
        request.user = self.user
        response = edit_reservation(request, pk=reservation.pk)
        self.assertEqual(response.status_code, 302)  # Redirects upon successful edit
