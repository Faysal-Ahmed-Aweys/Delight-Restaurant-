from django.db import models
from django.contrib.auth.models import User

class Reservation(models.Model):
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
        return f"{self.user.get_full_name()} - {self.date} at {self.time}"

    def clean(self):
        from django.core.exceptions import ValidationError
        from django.utils import timezone
        import pytz

        # Combine date and time into a single datetime object
        if self.date and self.time:
            tz = pytz.timezone('Europe/London')  # Adjust to your timezone
            datetime_combined = timezone.make_aware(datetime.combine(self.date, self.time), timezone=tz)

            # Validate that the reservation is in the future
            if datetime_combined <= timezone.now():
                raise ValidationError("Reservation date and time must be in the future.")
