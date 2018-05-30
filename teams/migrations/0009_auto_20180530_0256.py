# Generated by Django 2.0.5 on 2018-05-30 02:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0008_auto_20180529_2205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill',
            name='user_profile',
        ),
        migrations.AddField(
            model_name='skill',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='skills', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='otherproject',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='other_projects', to=settings.AUTH_USER_MODEL),
        ),
    ]
