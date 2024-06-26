from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ReservationForm, EditReservationForm
from .models import Reservation
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from datetime import date
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.http import HttpResponse
import logging

@login_required
def reserve(request):
    """
    Handles the reservation creation process for logged-in users. Staff members are redirected away from this view.

    If the request method is POST, attempts to create a new reservation. If successful, sends a confirmation email
    and displays a success message. If the reservation slot is already booked, displays an error message.

    If the request method is GET, displays the reservation form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered reservation form or a redirect to the profile page.
    """
    if request.user.is_staff:
        messages.warning(request, 'You are not authorized to view this page.')
        return redirect('staff_dashboard')

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation_date = form.cleaned_data['date']
            reservation_time = form.cleaned_data['time']
            num_people = form.cleaned_data['num_people']
            user = request.user

            if Reservation.objects.filter(date=reservation_date, time=reservation_time).exists():
                return render(request, 'reserve.html', {
                    'form': form,
                    'error_message': 'This reservation slot is already booked. Please choose another time.'
                })

            reservation = form.save(commit=False)
            reservation.user = user
            reservation.save()

            # Prepare email
            subject = 'Reservation Confirmation'
            context = {'reservation': reservation}
            email_template = render_to_string('reservation_confirmation_email.html', context)
            from_email = settings.EMAIL_HOST_USER
            to_email = user.email

            # Debugging Information
            print("Email Subject:", subject)
            print("Email Message:", email_template)
            print("From Email:", from_email)
            print("To Email:", to_email)

            try:
                # Send email
                send_mail(
                    subject,
                    email_template,
                    from_email,
                    [to_email],
                    fail_silently=False
                )
                print("Email sent successfully")
            except Exception as e:
                logging.error(f"Error sending email: {e}")

            messages.success(request, 'Reservation successfully made! A confirmation email has been sent.')

            return redirect('profile')
    else:
        form = ReservationForm()

    return render(request, 'reserve.html', {'form': form})

@login_required
def edit_reservation(request, pk):
    """
    Handles the reservation editing process for logged-in users.

    If the request method is POST, attempts to update the reservation. If successful, displays a success message.
    If the reservation slot is already booked, displays an error message.

    If the request method is GET, displays the reservation editing form.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the reservation to be edited.

    Returns:
        HttpResponse: The rendered reservation editing form or a redirect to the profile page.
    """
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
    """
    Handles the reservation cancellation process for logged-in users.

    If the request method is POST, deletes the reservation and displays a success message.

    If the request method is GET, displays the reservation cancellation confirmation form.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the reservation to be cancelled.

    Returns:
        HttpResponse: The rendered reservation cancellation confirmation form or a redirect to the profile page.
    """
    reservation = get_object_or_404(Reservation, id=pk)
    
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Reservation successfully cancelled!')
        return redirect('profile')  # Redirect to profile page after deletion
    
    # For GET request, render the confirmation page
    return render(request, 'cancel_reservation_confirmation.html', {'reservation': reservation})

@login_required
def delete_reservation(request, pk):
    """
    Handles the reservation deletion process for logged-in users.

    If the request method is POST, deletes the reservation and displays a success message.

    If the request method is GET, displays the reservation deletion confirmation form.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the reservation to be deleted.

    Returns:
        HttpResponse: The rendered reservation deletion confirmation form or a redirect to the profile page.
    """
    reservation = get_object_or_404(Reservation, id=pk)
    
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Reservation successfully deleted!')
        return redirect('profile')  # Redirect to profile page after deletion
    
    # For GET request, render the confirmation page
    return render(request, 'delete_reservation_confirmation.html', {'reservation': reservation})

def reservations_management(request):
    """
    Handles the reservation management view, allowing staff to search and filter reservations.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered reservations management page with filtered reservations.
    """
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

def edit_reservation_status(request, reservation_id):
    """
    Handles the editing of reservation status.

    Args:
        request (HttpRequest): The HTTP request object.
        reservation_id (int): The primary key of the reservation to be edited.

    Returns:
        HttpResponse: The rendered reservation status editing form or a redirect to the reservation management page.
    """
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        reservation.status = request.POST.get('status')
        reservation.save()
        messages.success(request, 'Reservation status updated.')
        return redirect('Manage_reservations')
    return render(request, 'edit_reservation_status.html', {'reservation': reservation})



def change_reservation_status(request, reservation_id, status):
    """
    Changes the status of a reservation to the specified status.

    Args:
        request (HttpRequest): The HTTP request object.
        reservation_id (int): The primary key of the reservation to have its status changed.
        status (str): The new status for the reservation ('approved', 'denied', 'pending').

    Returns:
        HttpResponse: A redirect to the reservation management page with a success or error message.
    """
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if status in ['approved', 'denied', 'pending']:
        reservation.status = status
        reservation.save()
        messages.success(request, f'Reservation {status}.')
    else:
        messages.error(request, 'Invalid status.')
    return redirect('Manage_reservations')
