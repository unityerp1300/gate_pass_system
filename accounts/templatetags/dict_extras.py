from django import template
from urllib.parse import urlencode

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Return dictionary[key] or None."""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None


@register.filter
def attr(obj, name):
    """Return getattr(obj, name) for templates."""
    try:
        return getattr(obj, name)
    except Exception:
        return None

@register.simple_tag(takes_context=True)
def query_without_page(context):
    """Return current GET params as query string, excluding 'page'."""
    request = context.get('request')
    if not request:
        return ''
    params = request.GET.copy()
    params.pop('page', None)
    return params.urlencode()
