from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UpdateUserForm
from reservations.models import Reservation
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required
def profile(request):
    """
    View function to display user profile with reservations.

    Retrieves upcoming and expired reservations for the current user,
    and renders the profile.html template with necessary data.

    Args:
        request: HTTP request object.

    Returns:
        Rendered template with upcoming_reservations, expired_reservations, and success_message context data.
    """
    user = request.user
    reservations = Reservation.objects.filter(user=user)

    current_datetime = datetime.now()
    
    upcoming_reservations = reservations.filter(date__gte=current_datetime.date()).exclude(date=current_datetime.date(), time__lte=current_datetime.time())

    expired_reservations = reservations.filter(Q(date__lt=current_datetime.date()) | (Q(date=current_datetime.date()) & Q(time__lt=current_datetime.time())))

    success_message = messages.get_messages(request)

    return render(request, 'profile.html', {
        'upcoming_reservations': upcoming_reservations,
        'expired_reservations': expired_reservations,
        'success_message': success_message,
    })

@login_required
def edit_profile(request, pk):
    """
    View function to edit user profile details.

    Retrieves the user object based on pk, handles form submission for updating user details,
    and renders the edit_details.html template with the user_form and user context data.

    Args:
        request: HTTP request object.
        pk: Primary key of the user to be edited.

    Returns:
        Rendered template with user_form and user context data on GET request.
        Redirects to the profile view on successful POST request.
    """
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your details have been updated successfully.')
            return redirect('profile')
    else:
        user_form = UpdateUserForm(instance=user)

    return render(request, 'edit_details.html', {'user_form': user_form, 'user': user})

@login_required
def delete_account_confirmation(request, pk):
    """
    View function to display delete account confirmation page.

    Retrieves the user object based on pk and renders the delete_account_confirmation.html template
    data for confirmation.

    Args:
        request: HTTP request object.
        pk: Primary key of the user account to be deleted.

    Returns:
        Rendered template for account deletion confirmation.
    """
    user = User.objects.get(pk=pk)
    return render(request, 'delete_account_confirmation.html', {'user': user})

@login_required
def delete_account(request, pk):
    """
    View function to handle account deletion.

    Retrieves the user object based on pk, handles POST request for account deletion confirmation,
    deletes the user account, logs out the user, adds a success message, and redirects to the home page.

    Args:
        request: HTTP request object.
        pk: Primary key of the user account to be deleted.

    Returns:
        Redirects to the home page on successful account deletion confirmation POST request.
        Redirects to the profile page on cancellation of deletion or invalid request.
    """
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        if request.POST.get('action') == 'confirm':
            user.delete()
            logout(request)
            messages.success(request, 'Your account has been successfully deleted.')
            return redirect('home')
        else:
            return redirect('profile')
    return render(request, 'delete_account_confirmation.html', {'user': user})

