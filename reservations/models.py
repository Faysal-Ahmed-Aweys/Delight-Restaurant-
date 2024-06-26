from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime

class Reservation(models.Model):
    """
    model for creating reservations

    Attributes:
    - user: The user who made the reservation.
    - date: The date of the reservation.
    - time: The time of the reservation.
    - num_people: The number of people for the reservation.
    - status: The status of the reservation (pending, approved, denied).

    Meta options:
    - unique_together: Ensures a user cannot have multiple reservations at the same date and time.
    - ordering: Orders reservations by date and time.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    num_people = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='approved')

    class Meta:
        unique_together = ['date', 'time', 'user']
        ordering = ['date', 'time']

    def __str__(self):
        """
        Returns a string representation of the reservation.
        """
        return f"{self.user.get_full_name()} - {self.date} at {self.time}"

    def clean(self):
        """
        Validates the reservation to ensure it is set in the future.

        Raises:
        - ValidationError: If the reservation date and time are not in the future.
        """
        datetime_combined = timezone.make_aware(
            datetime.combine(self.date, self.time),
            timezone=timezone.get_current_timezone()
        )

        # Validate that the reservation is in the future
        if datetime_combined <= timezone.now():
            raise ValidationError("Reservation date and time must be in the future.")
