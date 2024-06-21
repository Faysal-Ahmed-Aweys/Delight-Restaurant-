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
    user = request.user
    # Get all reservations for the current user
    reservations = Reservation.objects.filter(user=user)

    # Get current date and time
    current_datetime = datetime.now()
    
    # Filter upcoming reservations
    upcoming_reservations = reservations.filter(date__gte=current_datetime.date()).exclude(date=current_datetime.date(), time__lte=current_datetime.time())

    # Filter expired reservations
    expired_reservations = reservations.filter(Q(date__lt=current_datetime.date()) | (Q(date=current_datetime.date()) & Q(time__lt=current_datetime.time())))

    success_message = messages.get_messages(request)

    return render(request, 'profile.html', {
        'upcoming_reservations': upcoming_reservations,
        'expired_reservations': expired_reservations,
        'success_message': success_message,
    })

@login_required
def edit_profile(request, pk):
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
    user = User.objects.get(pk=pk)
    return render(request, 'delete_account_confirmation.html', {'user': user})

@login_required
def delete_account(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        if request.POST.get('action') == 'confirm':
            # Delete the user account
            user.delete()
            # Logout the user
            logout(request)
            # Add a success message
            messages.success(request, 'Your account has been successfully deleted.')
            # Redirect to the home page
            return redirect('home')
        else:
            # User canceled the deletion, redirect back to profile page
            return redirect('profile')
    return render(request, 'delete_account_confirmation.html', {'user': user})