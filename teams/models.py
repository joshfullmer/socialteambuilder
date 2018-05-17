from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        related_name="profile",
        on_delete=models.CASCADE)


class Project(models.Model):
    pass


class Position(models.Model):
    pass


class Application(models.Model):
    pass


class Notification(models.Model):
    pass
