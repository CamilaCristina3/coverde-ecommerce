from django import template

register = template.Library()

@register.filter(name='format_price')
def format_price(value):
    """Formata o preço para o formato monetário"""
    return f"€{value:,.2f}".replace(",", " ").replace(".", ",").replace(" ", ".")