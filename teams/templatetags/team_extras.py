from django import template
register = template.Library()


@register.filter(name='cssclass')
def cssclass(field, css):
    return field.as_widget(attrs={"class": css})
