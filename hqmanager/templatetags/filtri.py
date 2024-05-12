from django import template

register = template.Library()

@register.filter(name='add_bootstrap_class')
def add_bootstrap_class(value, arg):
    return value.as_widget(attrs={'class': arg})
