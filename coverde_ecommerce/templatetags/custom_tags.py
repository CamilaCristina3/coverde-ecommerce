from django import template

register = template.Library()

@register.simple_tag
def exemplo():
    return "Funcionando"
