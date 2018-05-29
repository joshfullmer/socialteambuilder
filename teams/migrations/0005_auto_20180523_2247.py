# Generated by Django 2.0.4 on 2018-05-23 22:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0004_projectposition_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='project_position',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='teams.ProjectPosition'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='response',
            field=models.CharField(default='rejected', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='status',
            field=models.CharField(default='unread', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]