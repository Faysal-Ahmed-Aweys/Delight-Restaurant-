from django.urls import path
from .views import reserve

urlpatterns = [
    path('reserve/', reserve, name='reserve'),
]