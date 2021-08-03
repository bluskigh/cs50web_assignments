from django import template
from auctions.models import Categories


register = template.Library()


@register.filter(name='mod_three')
def mod_three(value):
    return (value - 1) % 3


@register.filter(name='contains_query')
def contains_query(value):
    category = value.get('category')
    if category is None:
        return False
    return Categories.objects.get(id=category)
