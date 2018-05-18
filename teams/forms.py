from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import PasswordInput, TextInput, Textarea

from . import models


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


class UserProfileForm(forms.ModelForm):
    full_name = forms.CharField(
        label='',
        required=False,
        widget=TextInput(attrs={'placeholder': 'Full Name'}))
    description = forms.CharField(
        label='',
        required=False,
        widget=Textarea(attrs={'placeholder': 'Tell us about yourself...'}))
    avatar = forms.FileInput()

    class Meta:
        model = models.UserProfile
        fields = ['full_name', 'description', 'avatar']


class ProjectForm(forms.ModelForm):
    title = forms.CharField(
        label='',
        widget=TextInput(attrs={'placeholder': 'Project Title'}))
    description = forms.CharField(
        label='',
        widget=Textarea(attrs={'placeholder': 'Project description...'}))
    time_estimate = forms.CharField(
        label='',
        widget=Textarea(attrs={'placeholder': 'Time estimate'}))
    requirements = forms.CharField(
        label='',
        widget=Textarea())

    class Meta:
        model = models.Project
        fields = ['title', 'description', 'time_estimate', 'requirements']


class ProjectPositionForm(forms.ModelForm):
    id = forms.IntegerField(required=False)
    position = forms.ModelChoiceField(
        queryset=models.Position.objects.all(),
        empty_label="Please select one...")
    description = forms.CharField(
        label='',
        widget=Textarea(attrs={'placeholder': 'Position description...'}))

    class Meta:
        model = models.ProjectPosition
        fields = ['position', 'description']


ProjectPositionFormSet = forms.modelformset_factory(
    models.ProjectPosition,
    form=ProjectPositionForm,
    can_delete=True)
