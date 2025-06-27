from django import template

from predictionGame.bets.models import Wildcards

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def placeholder(value, token):
    value.field.widget.attrs['placeholder'] = token
    return value


@register.filter
def has_wildcard(user):
    return Wildcards.objects.filter(user=user).exists()


@register.filter
def get(champions, name):
    return champions.get(name)


@register.filter
def index(list_obj, i):
    try:
        return list_obj[i]
    except IndexError:
        return None
    
@register.filter
def times(number):
    return range(number)

