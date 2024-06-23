from django.shortcuts import render, redirect
from django.contrib import messages

def staff_dashboard(request):
    if request.user.is_staff:
        return render(request, 'staff_dashboard.html')
    else:
        messages.warning(
            request, ('You are not authorized to view this page')
            )
        return redirect('home')
