from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from . import models, forms


# Create your views here.
def home(request, position_pk=None):
    positions = models.Position.objects.all()
    if position_pk:
        project_positions = models.ProjectPosition.objects.filter(
            position__pk=position_pk)
    else:
        project_positions = models.ProjectPosition.objects.all()
    return render(
        request,
        'teams/home.html',
        {'positions': positions,
         'position_pk': position_pk,
         'project_positions': project_positions})


def sign_up(request):
    form = forms.PlaceholderSignUpForm()
    if request.method == 'POST':
        form = forms.PlaceholderSignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('teams:profile'))
    return render(request, 'teams/sign_up.html', {'form': form})


def login_user(request):
    form = forms.PlaceholderLoginForm()
    if request.method == 'POST':
        form = forms.PlaceholderLoginForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('teams:profile')  # TODO: go to profile
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'teams/login.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('teams:home'))


@login_required
def profile_detail(request):
    try:
        user_profile = models.UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        user_profile = None
    projects = models.Project.objects.filter(user=request.user)
    return render(
        request,
        'teams/profile.html',
        {'selected': 'profile',
         'user_profile': user_profile,
         'projects': projects})


@login_required
def profile_detail_with_pk(request, pk):
    user = get_object_or_404(models.User, pk=pk)
    try:
        user_profile = models.UserProfile.objects.get(user=user)
    except ObjectDoesNotExist:
        user_profile = None
    projects = models.Project.objects.filter(user=user)
    return render(
        request,
        'teams/user_profile.html',
        {'user': user,
         'user_profile': user_profile,
         'projects': projects})


@login_required
def profile_edit(request):
    new = True
    try:
        profile = models.UserProfile.objects.get(user=request.user)
        new = False
    except ObjectDoesNotExist:
        profile = None
    form = forms.UserProfileForm(instance=profile)
    if request.method == "POST":
        form = forms.UserProfileForm(
            request.POST,
            request.FILES,
            instance=profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return HttpResponseRedirect(reverse('teams:profile'))
    return render(
        request,
        'teams/profile_edit.html',
        {'selected': 'profile', 'form': form, 'new': new})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(models.Project, pk=pk)
    project_positions = models.ProjectPosition.objects.filter(project__pk=pk)
    project_owner = get_object_or_404(models.User, pk=project.user.pk)
    user_applications = models.Application.objects.filter(user=request.user)
    user_application_positions = [app.project_position.pk
                                  for app in user_applications]
    try:
        display_name = project_owner.profile.full_name
    except ObjectDoesNotExist:
        display_name = project_owner.username
    return render(
        request,
        'teams/project.html',
        {'project': project,
         'positions': project_positions,
         'project_owner': project_owner,
         'display_name': display_name,
         'user_apps': user_application_positions})


@login_required
def project_edit(request, pk=None):
    new = True
    if pk:
        try:
            project = models.Project.objects.get(pk=pk)
            project_positions = models.ProjectPosition.objects.filter(
                project=project)
            new = False
        except ObjectDoesNotExist:
            project = None
    else:
        project = None
        project_positions = models.ProjectPosition.objects.none()
    form = forms.ProjectForm(instance=project)
    formset = forms.ProjectPositionFormSet(queryset=project_positions)
    if request.method == "POST":
        form = forms.ProjectForm(
            request.POST,
            instance=project)
        formset = forms.ProjectPositionFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            new_project = form.save(commit=False)
            new_project.user = request.user
            new_project.save()
            instances = formset.save(commit=False)
            for obj in formset.deleted_objects:
                obj.delete()
            for each in instances:
                if not each.id:
                    models.ProjectPosition.objects.create(
                        project=new_project,
                        position=each.position,
                        description=each.description)
                else:
                    each.save()
            messages.success(
                request,
                f"Project \"{new_project.title}\" "
                f"{'created' if new else 'updated'}.")
            return HttpResponseRedirect(
                reverse('teams:project', args=(new_project.id,)))

    return render(
        request,
        'teams/project_edit.html',
        {'form': form, 'formset': formset, 'new': new})


@login_required
def project_delete(request, pk):
    project = get_object_or_404(models.Project, pk=pk)
    messages.success(request, f"Project \"{project.title}\" deleted.")
    project.delete()
    return HttpResponseRedirect(reverse('teams:home'))


@login_required
def apply(request, pk, project_position_pk):
    try:
        models.Application.objects.get(
            user=request.user,
            project_position__pk=project_position_pk)
    except ObjectDoesNotExist:
        project_position = get_object_or_404(
            models.ProjectPosition,
            pk=project_position_pk)
        models.Application.objects.create(
            user=request.user,
            project_position=project_position,
            status='new')
        messages.success(
            request,
            f"Thanks for applying for {project_position.position.title}")
        return HttpResponseRedirect(reverse(
            'teams:project',
            args=[pk]))
    else:
        messages.warning(request, "You have already applied for this position")
        return HttpResponseRedirect(reverse(
            'teams:project',
            args=[pk]))


@login_required
def application_list(request):
    projects = models.Project.objects.filter(user=request.user)
    positions = models.Position.objects.all()
    applications = models.Application.objects.filter(
        project_position__project__user=request.user)
    return render(
        request,
        'teams/applications.html',
        {'selected': 'applications',
         'projects': projects,
         'positions': positions,
         'applications': applications})


@login_required
def accept_application(request, pk):
    application = get_object_or_404(models.Application, pk=pk)
    application.status = "accepted"
    application.project_position.status = "filled"
    application.save()
    (models.Application.objects
        .filter(project_position=application.project_position)
        .exclude(pk=pk)
        .update(status="rejected"))
    (models.ProjectPosition.objects
        .filter(pk=application.project_position.pk)
        .update(status="filled"))
    return HttpResponseRedirect(reverse('teams:applications'))


@login_required
def reject_application(request, pk):
    application = get_object_or_404(models.Application, pk=pk)
    application.status = "rejected"
    application.save()
    return HttpResponseRedirect(reverse('teams:applications'))
