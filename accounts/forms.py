from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'motto', 'website', 'current_location']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'motto': forms.TextInput(attrs={'placeholder': 'Live and let live'}),
            'website': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
            'current_location': forms.TextInput(attrs={'placeholder': 'e.g., Montreal, Canada'}),
        }

