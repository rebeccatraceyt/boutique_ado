from django import template


register = template.Library()


# register filter decorator regististers function
# as template filter
@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """
        Takes price and quantity as parameters
        Returns their product
    """

    return price * quantity
