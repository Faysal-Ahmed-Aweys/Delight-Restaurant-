from django.urls import path
from .views import menu, add_menu_item, manage_menu_items

urlpatterns = [
    path('menu/', menu, name='menu'),
    path('menu/add_menu_item/', add_menu_item, name='add_menu_item'),
    path('menu/manage_menu_items/', manage_menu_items, name='manage_menu_items'),
]