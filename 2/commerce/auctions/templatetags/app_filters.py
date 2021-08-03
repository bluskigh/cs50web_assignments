from django import template


register = template.Library()


@register.filter(name='mod_three')
def mod_three(value):
    return (value - 1) % 3
