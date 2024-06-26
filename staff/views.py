from django.shortcuts import render, redirect
from django.contrib import messages

def staff_dashboard(request):
    """
    View function for the staff dashboard.

    This view checks if the user making the request is a staff member. If the user is a staff member,
    it renders the staff dashboard page. If the user is not a staff member, it adds a warning message
    indicating that the user is not authorized to view the page and redirects the user to the home page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered staff dashboard page if the user is a staff member.
        HttpResponseRedirect: A redirect to the home page if the user is not a staff member.
    """
    if request.user.is_staff:
        return render(request, 'staff_dashboard.html')
    else:
        messages.warning(request, 'You are not authorized to view this page')
        return redirect('home')
