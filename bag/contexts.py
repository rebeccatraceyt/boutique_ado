from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def bag_contents(request):
    """
    returns dictionary 'context' = context processor
        - makes dictionary availble to all templates across application
        - added to settings.py, under TEMPLATES/'OPTIONS'
    """

    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})
    # check if bag variable exists

    # for items/quantity in session 'bag'
    for item_id, item_data in bag.items():

        # checking whether item_data = int
        # if int = just quantity
        # if not int = includes size (dictionary)
        if isinstance(item_data, int):
            # get product
            product = get_object_or_404(Product, pk=item_id)

            # add  quantity to price for total
            total += item_data * product.price

            # increment product count by quantity
            product_count += item_data

            # bag items dictionary update
            bag_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            # iterate through inner dict
            # render sizes in template
            for size, quantity in item_data['items_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                bag_items.append({
                    'item_id': item_id,
                    'quantity': item_data,
                    'product': product,
                    'size': size,
                })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    
    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
