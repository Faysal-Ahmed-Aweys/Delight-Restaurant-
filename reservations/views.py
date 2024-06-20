from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ReservationForm
from .models import Reservation
from django.contrib import messages

@login_required
def reserve(request):
    if request.user.is_staff:  # Check if the user is staff
        messages.warning(request, 'You are not authorized to view this page.')
        return redirect('home')  # Redirect to staff dashboard or any other staff-related page

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation_date = form.cleaned_data['date']
            reservation_time = form.cleaned_data['time']
            num_people = form.cleaned_data['num_people']
            user = request.user

            # Check if the reservation already exists
            if Reservation.objects.filter(date=reservation_date, time=reservation_time).exists():
                return render(request, 'reserve.html', {
                    'form': form,
                    'error_message': 'This reservation slot is already booked. Please choose another time.'
                })

            reservation = form.save(commit=False)
            reservation.user = user
            reservation.save()

            # Set a success message
            messages.success(request, 'Reservation successfully made!')

            return redirect('home')
    else:
        form = ReservationForm()

    return render(request, 'reserve.html', {'form': form})
