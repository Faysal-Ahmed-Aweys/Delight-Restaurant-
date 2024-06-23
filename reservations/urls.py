from django.urls import path
from .views import reserve, edit_reservation, cancel_reservation, delete_reservation, reservations_management, edit_reservation_status, change_reservation_status

urlpatterns = [
    path('reserve/', reserve, name='reserve'),
    path('edit_reservation/<int:pk>/', edit_reservation, name='edit_reservation'),
    path('cancel_reservation_confirmation/<int:pk>/', cancel_reservation, name='cancel_reservation'),
    path('delete_reservation_confirmation/<int:pk>/', delete_reservation, name='delete_reservation'),
    path('manage/', reservations_management, name='Manage_reservations'),
    path('staff/edit_reservation/status/<int:reservation_id>/', edit_reservation_status, name='edit_reservation_status'),
    path('staff/change_reservation/status/<int:reservation_id>/<str:status>/', change_reservation_status, name='change_reservation_status'),
]