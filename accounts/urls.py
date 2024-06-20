from django.urls import path
from django.conf import settings
from .views import profile, delete_account_confirmation, delete_account, edit_profile

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('edit_profile/<int:pk>/', edit_profile, name='edit_profile'),
    path('delete_account_confirmation/<int:pk>/', delete_account_confirmation, name='delete_account_confirmation'),
    path('delete_account/<int:pk>/', delete_account, name='delete_account'),
]