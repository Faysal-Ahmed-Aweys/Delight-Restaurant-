from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuItem
from .forms import MenuItemForm
from itertools import chain
from django.contrib import messages
import cloudinary.uploader
import cloudinary.api
from cloudinary import CloudinaryImage

def menu(request):
    starters = MenuItem.objects.filter(category='starter')
    mains = MenuItem.objects.filter(category='main')
    desserts = MenuItem.objects.filter(category='dessert')

    combined_menu = list(chain(starters, mains, desserts))

    return render(request, 'menu.html', {
        'starters': starters,
        'mains': mains,
        'desserts': desserts,
        'combined_menu': combined_menu,
    })


def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item successfully added')
            return redirect('manage_menu_items')
    else:
        form = MenuItemForm()
    return render(request, 'add_menu_item.html', {'form': form})


def manage_menu_items(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'manage_menu_items.html', {'menu_items': menu_items})


def edit_menu_item(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item successfully edited')
            return redirect('manage_menu_items')
    else:
        form = MenuItemForm(instance=menu_item)
    return render(request, 'edit_menu_item.html', {'form': form})


def delete_menu_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Menu item successfully deleted')
        return redirect('manage_menu_items')
    return render(request, 'delete_menu_item.html', {'item': item})

