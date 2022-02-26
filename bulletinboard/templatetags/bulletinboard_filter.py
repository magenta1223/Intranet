from django import template

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def indexing(value, index):
    return value[index]