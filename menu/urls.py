from django.urls import path
from .views import menu, add_menu_item

urlpatterns = [
    path('menu/', menu, name='menu'),
    path('menu/add_menu_item/', add_menu_item, name='add_menu_item'),
]