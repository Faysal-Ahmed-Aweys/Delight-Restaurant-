from django.shortcuts import render, redirect

def home(request):
    """
    Render the home page based on user's staff status.

    If the user is a staff member, redirect to 'staff_dashboard'.
    Otherwise, render the 'index.html' template.

    Parameters:
    - request: HttpRequest object containing metadata about the request.

    Returns:
    - HttpResponse: Redirect to 'staff_dashboard' if user is staff, or render 'index.html' otherwise.
    """
    if request.user.is_staff:
        return redirect('staff_dashboard')
    else:
        return render(request, 'index.html')
