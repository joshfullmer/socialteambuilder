from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.widgets import PasswordInput, TextInput, Textarea

from . import models


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label='',
        widget=TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(
        label='',
        widget=PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(
        label='',
        widget=PasswordInput(attrs={'placeholder': 'Verify Password'}))


class LoginForm(AuthenticationForm):
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
        fields = ['full_name', 'description', 'avatar', 'positions']


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
    duration = forms.CharField(
        label='',
        widget=TextInput(attrs={'placeholder': 'Expected participation...'}))

    class Meta:
        model = models.ProjectPosition
        fields = ['position', 'description', 'duration']


ProjectPositionFormSet = forms.modelformset_factory(
    models.ProjectPosition,
    form=ProjectPositionForm,
    can_delete=True)


class SkillForm(forms.ModelForm):
    id = forms.IntegerField(required=False)
    name = forms.CharField(
        label='',
        widget=TextInput(attrs={'placeholder': 'Skill'}))

    class Meta:
        model = models.Skill
        fields = ['name', ]


SkillFormSet = forms.inlineformset_factory(
    models.User,
    models.Skill,
    form=SkillForm,
    extra=1,
    can_delete=True)


class OtherProjectForm(forms.ModelForm):
    id = forms.IntegerField(required=False)
    name = forms.CharField(
        label='',
        widget=TextInput(attrs={'placeholder': 'Project Name'}))
    url = forms.URLField(
        label='',
        widget=TextInput(attrs={'placeholder': 'Project URL'}))

    class Meta:
        model = models.OtherProject
        fields = ['name', 'url']


OtherProjectFormSet = forms.inlineformset_factory(
    models.User,
    models.OtherProject,
    form=OtherProjectForm,
    extra=1,
    can_delete=True)
