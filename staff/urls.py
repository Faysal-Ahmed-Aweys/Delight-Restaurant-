from django.urls import path
from .views import staff_dashboard

urlpatterns = [
    path('staff_dashboard/', staff_dashboard, name='staff_dashboard'),
]