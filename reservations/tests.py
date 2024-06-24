from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import date, time
from .models import Reservation
from .forms import ReservationForm, EditReservationForm
from .views import reserve, edit_reservation, cancel_reservation, delete_reservation

class ReservationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.reservation = Reservation.objects.create(
            user=self.user,
            date=date.today(),
            time=time(12, 0),
            num_people=4,
            status='approved'
        )

    def test_reservation_creation(self):
        self.assertEqual(self.reservation.user.username, 'testuser')
        self.assertEqual(self.reservation.date, date.today())
        self.assertEqual(self.reservation.time, time(12, 0))
        self.assertEqual(self.reservation.num_people, 4)
        self.assertEqual(self.reservation.status, 'approved')

    def test_unique_together_constraint(self):
        with self.assertRaises(Exception):
            Reservation.objects.create(
                user=self.user,
                date=date.today(),
                time=time(12, 0),
                num_people=2,
                status='approved'
            )

class ReservationFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_reservation_form_valid(self):
        form_data = {
            'date': date.today(),
            'time': '12:00',
            'num_people': 4,
        }
        form = ReservationForm(data=form_data)
        form.user = self.user
        self.assertTrue(form.is_valid() == False)

    def test_reservation_form_invalid_past_date(self):
        past_date = date.today()
        past_time = '10:00'
        form_data = {
            'date': past_date,
            'time': past_time,
            'num_people': 2,
        }
        form = ReservationForm(data=form_data)
        form.user = self.user
        self.assertFalse(form.is_valid())

class EditReservationFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.reservation = Reservation.objects.create(
            user=self.user,
            date=date.today(),
            time=time(12, 0),
            num_people=4,
            status='approved'
        )

    def test_edit_reservation_form_valid(self):
        form_data = {
            'date': date.today(),
            'time': '14:00',
            'num_people': 3,
        }
        form = EditReservationForm(data=form_data, instance=self.reservation)
        form.user = self.user
        self.assertTrue(form.is_valid() == False)

    def test_edit_reservation_form_invalid_past_date(self):
        past_date = date.today()
        past_time = '10:00'
        form_data = {
            'date': past_date,
            'time': past_time,
            'num_people': 2,
        }
        form = EditReservationForm(data=form_data, instance=self.reservation)
        form.user = self.user
        self.assertFalse(form.is_valid())

class ReservationViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_reserve_view_get(self):
        request = self.factory.get(reverse('reserve'))
        request.user = self.user
        response = reserve(request)
        self.assertEqual(response.status_code, 200)

    def test_reserve_view_post_valid(self):
        request = self.factory.post(reverse('reserve'), {
            'date': date.today(),
            'time': '14:00',
            'num_people': 3,
        })
        request.user = self.user
        response = reserve(request)
        self.assertEqual(response.status_code, 302)  # Redirects upon successful reservation

    def test_reserve_view_post_invalid_past_date(self):
        request = self.factory.post(reverse('reserve'), {
            'date': date.today(),
            'time': '10:00',
            'num_people': 2,
        })
        request.user = self.user
        response = reserve(request)
        self.assertEqual(response.status_code, 200)  # Renders the form again

    def test_edit_reservation_view_get(self):
        reservation = Reservation.objects.create(
            user=self.user,
            date=date.today(),
            time=time(12, 0),
            num_people=4,
            status='approved'
        )
        request = self.factory.get(reverse('edit_reservation', args=[reservation.pk]))
        request.user = self.user
        response = edit_reservation(request, pk=reservation.pk)
        self.assertEqual(response.status_code, 200)

    def test_edit_reservation_view_post_valid(self):
        reservation = Reservation.objects.create(
            user=self.user,
            date=date.today(),
            time=time(12, 0),
            num_people=4,
            status='approved'
        )
        request = self.factory.post(reverse('edit_reservation', args=[reservation.pk]), {
            'date': date.today(),
            'time': '14:00',
            'num_people': 3,
        })
        request.user = self.user
        response = edit_reservation(request, pk=reservation.pk)
        self.assertEqual(response.status_code, 302)  # Redirects upon successful edit
