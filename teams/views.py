from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse

from . import models, forms
from .tokens import account_activation_token


# Create your views here.
def home(request, position_pk=None, fillable=None):
    if request.user.is_authenticated:
        user_applications = models.Application.objects.filter(
            user=request.user)
        user_application_positions = [app.project_position.pk
                                      for app in user_applications]
    else:
        user_application_positions = None
    positions = models.Position.objects.all()
    if position_pk:
        project_positions = models.ProjectPosition.objects.filter(
            position__pk=position_pk)
    else:
        project_positions = models.ProjectPosition.objects.all()
    if fillable and request.user.is_authenticated:
        user_profile = models.UserProfile.objects.get(user=request.user)
        project_positions = project_positions.filter(
            position__in=user_profile.positions.all())
    return render(
        request,
        'teams/home.html',
        {'positions': positions,
         'position_pk': position_pk,
         'fillable': fillable,
         'project_positions': project_positions,
         'user_apps': user_application_positions})


def search(request):
    query = request.GET.get('q')
    print(query)
    if request.user.is_authenticated:
        user_applications = models.Application.objects.filter(
            user=request.user)
        user_application_positions = [app.project_position.pk
                                      for app in user_applications]
    else:
        user_application_positions = None
    positions = models.Position.objects.all()
    project_positions = (models.ProjectPosition.objects.filter(
        project__title__contains=query) |
        models.ProjectPosition.objects.filter(
            project__description__contains=query))
    return render(
        request,
        'teams/home.html',
        {'positions': positions,
         'project_positions': project_positions,
         'user_apps': user_application_positions,
         'query': query})


def sign_up(request):
    form = forms.SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            site = get_current_site(request)
            mail_subject = "Activate your Circle account."
            message = render_to_string(
                'teams/email_verification.html',
                {'user': user,
                 'domain': site.domain,
                 'uid': user.pk,
                 'token': account_activation_token.make_token(user)}
            )
            email = EmailMessage(mail_subject, message, to=["test@test.com"])
            email.send()
            messages.success(
                request,
                "Thanks for signing up!  Please check your email and verify.")
            return HttpResponseRedirect(reverse('teams:home'))
            """user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )"""
            return HttpResponseRedirect(reverse('teams:profile'))
    return render(request, 'teams/sign_up.html', {'form': form})


def activate(request, uid, token):
    try:
        user = models.User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse('teams:home'))
    else:
        messages.error(request, "Activation link is invalid.")
        return HttpResponseRedirect(reverse('teams:home'))


def login_user(request):
    form = forms.LoginForm()
    if request.method == 'POST':
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('teams:profile')
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
    skills = models.Skill.objects.filter(user=request.user)
    other_projects = models.OtherProject.objects.filter(
        user=request.user)
    return render(
        request,
        'teams/profile.html',
        {'selected': 'profile',
         'user_profile': user_profile,
         'projects': projects,
         'skills': skills,
         'other_projects': other_projects})


def profile_detail_with_pk(request, pk):
    user = get_object_or_404(models.User, pk=pk)
    skills = models.Skill.objects.filter(user=user)
    other_projects = models.OtherProject.objects.filter(user=user)
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
         'projects': projects,
         'skills': skills,
         'other_projects': other_projects})


@login_required
def profile_edit(request):
    new = True
    try:
        profile = models.UserProfile.objects.get(user=request.user)
        new = False
    except ObjectDoesNotExist:
        profile = None
    form = forms.UserProfileForm(instance=profile)
    skill_formset = forms.SkillFormSet(instance=request.user)
    other_project_formset = forms.OtherProjectFormSet(
        instance=request.user)
    if request.method == "POST":
        form = forms.UserProfileForm(
            request.POST,
            request.FILES,
            instance=profile)
        skill_formset = forms.SkillFormSet(
            request.POST,
            instance=request.user)
        other_project_formset = forms.OtherProjectFormSet(
            request.POST,
            instance=request.user)
        if (form.is_valid() and
                skill_formset.is_valid() and
                other_project_formset.is_valid()):
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            form.save_m2m()
            skill_instances = skill_formset.save(commit=False)
            for obj in skill_formset.deleted_objects:
                obj.delete()
            for each in skill_instances:
                if not each.id:
                    models.Skill.objects.create(
                        user=request.user,
                        name=each.name)
                else:
                    each.save()
            other_project_instances = other_project_formset.save(commit=False)
            for obj in other_project_formset.deleted_objects:
                obj.delete()
            for each in other_project_instances:
                if not each.id:
                    models.OtherProject.objects.create(
                        user=request.user,
                        name=each.name,
                        url=each.url)
                else:
                    each.save()
            return HttpResponseRedirect(reverse('teams:profile'))
    return render(
        request,
        'teams/profile_edit.html',
        {'selected': 'profile',
         'form': form,
         'new': new,
         'skill_formset': skill_formset,
         'other_project_formset': other_project_formset})


def project_detail(request, pk):
    project = get_object_or_404(models.Project, pk=pk)
    project_positions = models.ProjectPosition.objects.filter(project__pk=pk)
    project_owner = get_object_or_404(models.User, pk=project.user.pk)
    if request.user.is_authenticated:
        user_applications = models.Application.objects.filter(
            user=request.user)
        user_application_positions = [app.project_position.pk
                                      for app in user_applications]
    else:
        user_applications = None
        user_application_positions = None
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
                        description=each.description,
                        duration=each.duration)
                else:
                    each.save()
            formset.save_m2m()
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
    app_query = {'project_position__project__user': request.user}
    if request.GET.get('project') and request.GET.get('project') != 'all':
        app_query['project_position__project__pk'] = request.GET.get('project')
    if request.GET.get('status') and request.GET.get('status') != 'all':
        app_query['status'] = request.GET.get('status')
    if request.GET.get('position') and request.GET.get('position') != 'all':
        app_query['project_position__position__pk'] = request.GET.get(
            'position')
    projects = models.Project.objects.filter(user=request.user)
    positions = models.Position.objects.all()
    print(app_query)
    applications = models.Application.objects.filter(**app_query)
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
    rejected_apps = (models.Application.objects.filter(
        project_position=application.project_position,
        status="rejected")
    ).exclude(pk=pk)
    for app in rejected_apps:
        try:
            models.Notification.objects.get(
                user=app.user,
                project_position=app.project_position,
                response='rejected')
        except ObjectDoesNotExist:
            models.Notification.objects.create(
                user=app.user,
                project_position=app.project_position,
                response="rejected")
    (models.ProjectPosition.objects
        .filter(pk=application.project_position.pk)
        .update(status="filled"))
    models.Notification.objects.create(
        user=application.user,
        status='unread',
        response='approved',
        project_position=application.project_position)
    return HttpResponseRedirect(reverse('teams:applications'))


@login_required
def reject_application(request, pk):
    application = get_object_or_404(models.Application, pk=pk)
    application.status = "rejected"
    application.save()
    models.Notification.objects.create(
        user=application.user,
        status='unread',
        response='rejected',
        project_position=application.project_position)
    return HttpResponseRedirect(reverse('teams:applications'))


@login_required
def notifications(request):
    notifications = models.Notification.objects.filter(user=request.user)
    status = request.GET.get('status', 'unread')
    if status != 'all':
        notifications = notifications.filter(status=status)
    return render(
        request,
        "teams/notifications.html",
        {'selected': 'notifications',
         'notifications': notifications,
         'status': status})


@login_required
def mark_as_read(request):
    notifications = models.Notification.objects.filter(user=request.user)
    for notif in notifications:
        notif.status = "read"
        notif.save()
    return HttpResponseRedirect(reverse('teams:notifications'))
