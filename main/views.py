from django.shortcuts import render, redirect

def home(request):
    if request.user.is_staff:
        return redirect('staff_dashboard')
    else:
        return render(request, 'index.html')