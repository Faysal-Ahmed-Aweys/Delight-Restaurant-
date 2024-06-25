from django.test import TestCase
from django.urls import reverse
from .models import MenuItem
from .forms import MenuItemForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User


class MenuItemModelTest(TestCase):
    """
    Test cases for the MenuItem model.
    """

    def setUp(self):
        """
        Set up a sample MenuItem instance for testing.
        """
        self.menu_item = MenuItem.objects.create(
            name='Test Item',
            description='Test description',
            price=9.99,
            category='starter',
            image='test_image.jpg'
        )

    def test_menu_item_creation(self):
        """
        Test the creation of a MenuItem instance.
        """
        self.assertEqual(self.menu_item.name, 'Test Item')
        self.assertEqual(self.menu_item.description, 'Test description')
        self.assertEqual(float(self.menu_item.price), 9.99)
        self.assertEqual(self.menu_item.category, 'starter')
        self.assertEqual(self.menu_item.image, 'test_image.jpg')

    def test_menu_item_str(self):
        """
        Test the string representation of a MenuItem instance.
        """
        self.assertEqual(str(self.menu_item), 'Test Item')


class MenuItemFormTest(TestCase):
    """
    Test cases for the MenuItemForm.
    """

    def test_valid_form(self):
        """
        Test the MenuItemForm with valid data.
        """
        form_data = {
            'name': 'New Item',
            'description': 'New description',
            'price': 12.99,
            'category': 'main',
        }
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        form = MenuItemForm(data=form_data, files={'image': image})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """
        Test the MenuItemForm with invalid data.
        """
        form_data = {}
        form = MenuItemForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)


class MenuViewsTest(TestCase):
    """
    Test cases for views related to MenuItem.
    """

    def setUp(self):
        """
        Set up a sample user and MenuItem instance for testing.
        """
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.client.login(username='testuser', password='password')
        self.menu_item = MenuItem.objects.create(
            name='Test Item',
            description='Test description',
            price=9.99,
            category='starter',
            image='test_image.jpg'
        )

    def test_menu_view(self):
        """
        Test the menu view.
        """
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu.html')

    def test_add_menu_item_view(self):
        """
        Test the add menu item view.
        """
        response = self.client.get(reverse('add_menu_item'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_menu_item.html')

    def test_manage_menu_items_view(self):
        """
        Test the manage menu items view.
        """
        response = self.client.get(reverse('manage_menu_items'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage_menu_items.html')

    def test_edit_menu_item_view(self):
        """
        Test the edit menu item view.
        """
        response = self.client.get(reverse('edit_menu_item', args=[self.menu_item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_menu_item.html')

    def test_delete_menu_item_view(self):
        """
        Test the delete menu item view.
        """
        response = self.client.get(reverse('delete_menu_item', args=[self.menu_item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_menu_item.html')

    def test_add_menu_item_form_valid(self):
        """
        Test form submission for adding a new menu item with valid data.
        """
        form_data = {
            'name': 'New Item',
            'description': 'New description',
            'price': 12.99,
            'category': 'main',
        }
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.post(reverse('add_menu_item'), data=form_data, files={'image': image})
        self.assertEqual(response.status_code, 302)

    def test_edit_menu_item_form_valid(self):
        """
        Test form submission for editing an existing menu item with valid data.
        """
        form_data = {
            'name': 'Edited Item',
            'description': 'Edited description',
            'price': 15.99,
            'category': 'dessert',
        }
        response = self.client.post(reverse('edit_menu_item', args=[self.menu_item.id]), data=form_data)
        self.assertEqual(response.status_code, 302)

    def test_delete_menu_item(self):
        """
        Test the deletion of a menu item.
        """
        response = self.client.post(reverse('delete_menu_item', args=[self.menu_item.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(MenuItem.objects.filter(id=self.menu_item.id).exists())
