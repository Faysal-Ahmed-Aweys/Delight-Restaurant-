from django.shortcuts import render
from .models import MenuItem
from itertools import chain

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
