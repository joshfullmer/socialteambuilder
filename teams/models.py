from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name="profile",
        on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    description = models.TextField()
    avatar = models.ImageField(default='', upload_to='./avatars')


class Skill(models.Model):
    user = models.ForeignKey(
        User,
        related_name="skills",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)


class OtherProject(models.Model):
    """Only for the user profile, not affiliated with Circle projects"""
    user = models.ForeignKey(
        User,
        related_name="other_projects",
        on_delete=models.CASCADE,)
    name = models.CharField(max_length=50)
    url = models.URLField()


class Position(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Project(models.Model):
    user = models.ForeignKey(
        User,
        related_name='projects',
        on_delete=models.CASCADE,)
    title = models.CharField(max_length=100)
    description = models.TextField()
    time_estimate = models.TextField()
    requirements = models.TextField()
    positions = models.ManyToManyField(Position, through='ProjectPosition')


class ProjectPosition(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    description = models.TextField()


class Application(models.Model):
    pass


class Notification(models.Model):
    pass
