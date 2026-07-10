from django import template

register = template.Library()


@register.filter(name='inr')
def inr(value):
    """
    Formats a number as Indian Rupees with standard comma grouping and ₹ symbol.
    Usage in templates: {{ some_amount|inr }}
    Note: uses standard (Western) comma grouping for simplicity in Phase 2.
    Indian-style lakh/crore grouping (e.g. 1,00,000) can be added later if desired.
    """
    if value is None:
        return '₹0.00'
    try:
        value = float(value)
    except (ValueError, TypeError):
        return value
    return f'₹{value:,.2f}'
