from django import forms
from django.contrib.auth.models import User 
from django.utils import timezone
import pytz
from pytz import utc
from datetime import datetime, timedelta, time as dt_time
from .models import Reservation

class ReservationForm(forms.ModelForm):
    """
    Form for creating a new reservation.

    Fields:
    - date: Date of the reservation with a minimum set to tomorrow's date.
    - time: Time of the reservation with options from 9:00 to 20:00.
    - num_people: Number of people for the reservation, ranging from 1 to 6.
    """
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'min': (timezone.now() + timedelta(days=1)).date()}))
    time = forms.ChoiceField(choices=[], widget=forms.Select())
    num_people = forms.ChoiceField(choices=[(i, i) for i in range(1, 7)])

    class Meta:
        model = Reservation
        fields = ['date', 'time', 'num_people']

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['time'].choices = self.generate_time_options()
        self.initial['date'] = (timezone.now() + timedelta(days=1)).date()

        if self.instance and self.instance.time:
            reservation_time = self.instance.time.strftime("%H:%M")
            self.initial['time'] = reservation_time

    def generate_time_options(self):
        """
        Generate available time options for the reservation.
        """
        time_options = []
        for hour in range(9, 21):
            time_options.append((f"{hour:02d}:00", f"{hour:02d}:00"))
        return time_options

    def clean(self):
        """
        Validate the form data.
        Ensure the selected date and time are in the future.
        """
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time_str = cleaned_data.get("time")

        if date and time_str:
            selected_time = time_str.split(":")
            time_object = dt_time(int(selected_time[0]), int(selected_time[1]))

            tz = pytz.timezone('Europe/London')
            datetime_combined = datetime.combine(date, time_object).replace(tzinfo=tz)
            if datetime_combined <= timezone.now():
                raise forms.ValidationError("Please select a future time.")
        
        return cleaned_data

class EditReservationForm(forms.ModelForm):
    """
    Form for editing an existing reservation.

    Fields:
    - date: Date of the reservation with a minimum set to tomorrow's date.
    - time: Time of the reservation with options from 9:00 to 20:00.
    - num_people: Number of people for the reservation, ranging from 1 to 6.
    """
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.ChoiceField(choices=[], widget=forms.Select())
    num_people = forms.ChoiceField(choices=[(i, i) for i in range(1, 7)])

    class Meta:
        model = Reservation
        fields = ['date', 'time', 'num_people']

    def __init__(self, *args, **kwargs):
        super(EditReservationForm, self).__init__(*args, **kwargs)
        self.fields['time'].choices = self.generate_time_options()

        if self.instance and self.instance.time:
            reservation_time = self.instance.time.strftime("%H:%M")
            self.initial['time'] = reservation_time

        today = timezone.now().date()
        tomorrow = today + timedelta(days=1)
        self.fields['date'].widget.attrs['min'] = tomorrow.strftime('%Y-%m-%d')

    def generate_time_options(self):
        """
        Generate available time options for the reservation.
        """
        time_options = []

        for hour in range(9, 21):
            time_options.append(
                (
                    f"{hour:02d}:00",
                    f"{hour:02d}:00"
                )
            )

        return time_options

    def clean(self):
        """
        Validate the form data.
        Ensure the selected date and time are in the future.
        """
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")

        if date and time:
            tz = pytz.timezone('Europe/London')
            datetime_combined = datetime.combine(date, datetime.strptime(time, '%H:%M').time()).replace(tzinfo=tz)
            if datetime_combined <= timezone.now():
                raise forms.ValidationError("Please select a future time.")
        
        return cleaned_data
