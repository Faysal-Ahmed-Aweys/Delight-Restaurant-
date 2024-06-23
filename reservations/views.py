from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReservationForm, EditReservationForm
from .models import Reservation
from django.contrib import messages
from django.db.models import Q
from datetime import date

@login_required
def reserve(request):
    if request.user.is_staff:  # Check if the user is staff
        messages.warning(request, 'You are not authorized to view this page.')
        return redirect('staff_dashboard')  # Redirect to staff dashboard

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

            return redirect('profile')
    else:
        form = ReservationForm()

    return render(request, 'reserve.html', {'form': form})

@login_required
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    error_message = None
    user = request.user

    if request.method == 'POST':
        form = EditReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            # Get the original status before saving the form
            original_status = reservation.status

            reservation_date = form.cleaned_data['date']
            reservation_time = form.cleaned_data['time']

            # Check if the reservation already exists excluding the current reservation
            if Reservation.objects.filter(date=reservation_date, time=reservation_time).exclude(pk=pk).exists():
                error_message = 'This reservation slot is already booked. Please choose another time.'
            else:
                # Save the form
                form.save()
                messages.success(request, 'Reservation successfully updated!')

                return redirect('profile')
    else:
        form = EditReservationForm(instance=reservation)

    return render(request, 'edit_reservation.html', {
        'form': form,
        'reservation': reservation,
        'user': user,
        'error_message': error_message
    })

@login_required
def cancel_reservation(request, pk):
    reservation = get_object_or_404(Reservation, id=pk)
    
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Reservation successfully cancelled!')
        return redirect('profile')  # Redirect to profile page after deletion
    
    # For GET request, render the confirmation page
    return render(request, 'cancel_reservation_confirmation.html', {'reservation': reservation})

@login_required
def delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, id=pk)
    
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Reservation successfully deleted!')
        return redirect('profile')  # Redirect to profile page after deletion
    
    # For GET request, render the confirmation page
    return render(request, 'delete_reservation_confirmation.html', {'reservation': reservation})


def reservations_management(request):
    reservations = Reservation.objects.all()

    search_name = request.GET.get('search_name')
    search_date = request.GET.get('search_date')
    search_today = request.GET.get('search_today')
    search_status = request.GET.get('search_status')

    if search_name:
        reservations = reservations.filter(Q(user__first_name__icontains=search_name) | Q(user__last_name__icontains=search_name))
    
    if search_date:
        reservations = reservations.filter(date=search_date)
    
    if search_today:
        reservations = reservations.filter(date=date.today())
    
    if search_status:
        reservations = reservations.filter(status=search_status)

    return render(request, 'reservations_management.html', {
        'reservations': reservations,
        'search_name': search_name,
        'search_date': search_date,
        'search_today': search_today,
        'search_status': search_status,
    })
