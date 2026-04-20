from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Acessa dict por chave no template: dict|get_item:key"""
    return dictionary.get(key)


@register.filter
def abs(value):
    import builtins
    return builtins.abs(value)
