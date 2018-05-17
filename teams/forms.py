from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import PasswordInput, TextInput


class PlaceholderSignUpForm(UserCreationForm):
    username = forms.CharField(
        label='',
        widget=TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(
        label='',
        widget=PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(
        label='',
        widget=PasswordInput(attrs={'placeholder': 'Verify Password'}))


class PlaceholderLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        widget=TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(
        label='',
        widget=PasswordInput(attrs={'placeholder': 'Password'}))
