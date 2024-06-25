from django import forms
from django.contrib.auth.models import User 
from allauth.account.forms import SignupForm, LoginForm

class CustomSignupForm(SignupForm):
    """
    Custom signup form extending Allauth's SignupForm to include first_name and last_name fields.

    Attributes:
        first_name (forms.CharField): Field for user's first name.
        last_name (forms.CharField): Field for user's last name.
    """

    first_name = forms.CharField(max_length=30, label='First Name', required=True)
    last_name = forms.CharField(max_length=30, label='Last Name', required=True)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class CustomLoginForm(LoginForm):
    """
    Custom login form extending Allauth's LoginForm to customize the login field label.

    Methods:
        __init__(*args, **kwargs): Initializes the form and customizes the 'login' field label.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = 'Email / Username'

class UpdateUserForm(forms.ModelForm):
    """
    Form for updating user information.

    Inherits from Django's ModelForm for the User model and adds custom validation for unique usernames and emails.

    Methods:
        clean_username(): Custom validation to ensure username uniqueness.
        clean_email(): Custom validation to ensure email uniqueness.
    """
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.user_id = kwargs['instance'].id

    def clean_username(self):
        username = self.cleaned_data.get('username').lower()
        if User.objects.filter(username__iexact=username).exclude(id=self.user_id).exists():
            raise forms.ValidationError("This username is already taken. Please choose a different one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email__iexact=email).exclude(id=self.user_id).exists():
            raise forms.ValidationError("This email is already registered. Please choose a different one.")
        return email