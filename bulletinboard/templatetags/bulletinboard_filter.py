from django import template

register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def parse(value, key):
    if key == '수량':
        return f'{value[0]} 개'
    else:
        return f'{value[0]} 원'
