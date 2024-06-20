from django.urls import path
from .views import reserve, edit_reservation, cancel_reservation

urlpatterns = [
    path('reserve/', reserve, name='reserve'),
    path('edit_reservation/<int:pk>/', edit_reservation, name='edit_reservation'),
    path('cancel_reservation_confirmation/<int:pk>/', cancel_reservation, name='cancel_reservation'),
]