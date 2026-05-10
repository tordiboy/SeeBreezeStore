from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control'
        })
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email Address',
            'class': 'form-control'
        })
    )

    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Phone Number',
            'class': 'form-control'
        })
    )

    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Home Address',
            'class': 'form-control',
            'rows': 3
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'phone',
            'address',
            'password1',
            'password2'
        )