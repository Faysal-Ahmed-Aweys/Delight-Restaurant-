from django.db import models
from cloudinary.models import CloudinaryField
import cloudinary

class MenuItem(models.Model):
    """
    Model representing an item on the menu.

    Attributes:
    ----------
    CATEGORY_CHOICES : list
        List of tuples representing the categories an item can belong to.
    name : str
        Name of the menu item.
    description : str
        Description of the menu item.
    price : decimal
        Price of the menu item, with a maximum of 5 digits and 2 decimal places.
    category : str
        Category of the menu item, chosen from CATEGORY_CHOICES.
    image : CloudinaryField
        Image of the menu item, stored using Cloudinary.

    Methods:
    -------
    __str__():
        Returns the name of the menu item.
    """

    CATEGORY_CHOICES = [
        ('starter', 'Starter'),
        ('main', 'Main'),
        ('dessert', 'Dessert'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    image = CloudinaryField('image')

    def __str__(self):
        return self.name
