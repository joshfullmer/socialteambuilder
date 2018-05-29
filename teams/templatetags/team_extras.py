from django import template
from markdown import markdown

from teams import models

register = template.Library()


@register.filter(name='cssclass')
def cssclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter(name='get')
def get(dix, key):
    return dix.get(key, '')


@register.simple_tag
def notification_count(user):
    return models.Notification.objects.filter(
        user=user, status="unread"
    ).count()


@register.filter(name='to_markdown')
def to_markdown(text):
    return markdown(text)
