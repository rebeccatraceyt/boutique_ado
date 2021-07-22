from django.http import HttpResponse

from .models import Order, OrderLineItem
from products.models import Product

import json
import time


class StripeWH_Handler:
    """Handle Stripe Webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """

        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle payment_intent.succeeded webhook from Stripe
        Ensure orders are entered in database
            - even if there is a user error
        """
        # intended event - checkout
        intent = event.data.object

        # payment intent id
        pid = intent.id
        # shopping bag
        bag = intent.metadata.bag
        # check whether save info is checked
        save_info = intent.metadata.save_info

        # order information to use:
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean data in the shipping details
        # replace empty strings in shipping details with none
        # avoid storing as blank string, not null value
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Check if order exists
        # if exists - return response
        # if does not - create it in the webhook
        order_exists = False

        # introduce delay to order creation
        # for when it isn't found in
        attempt = 1
        while attempt <= 5:
            try: 
                # get order info from payment intent
                # iexact lookup field makes sure it is an exact match
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )

                # if order is found:
                order_exists = True

                # if the order is found, break the loop
                break

            except Order.DoesNotExist:

                # increment attempt by 1
                attempt += 1

                # python time module to sleep for one second
                # webhook searchs for order five time in five seconds
                time.sleep(1)

        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:
                # creates form to save in webhook to create order
                # objects.create useing data from payment intent
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                # load bag from json verious in payment intent
                for item_id, item_data in json.loads(bag).items():
                    # get product id out of bag
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        # if product value is integer, there are no sizes
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        # else, if product has size
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(content=f'Webhook received: {event["type"]} | Error: {e}',
                status=500)


        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
