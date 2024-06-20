from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter your email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username here'}),
        }


class ForgotForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=100,
        required=True,
    )

    class Meta:
        model = User
        fields = ['email']
