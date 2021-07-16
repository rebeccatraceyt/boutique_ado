from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from bag.contexts import bag_contents

import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There is nothing in your bag at the moment")
        return redirect(reverse('products'))

    # get bag dictionary (make sure not to override bag)
    current_bag = bag_contents(request)

    # get bag total key
    total = current_bag['grand_total']

    # x100 and rounded to 0.00 (stripe requires interger)
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    print(intent)

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51JDxKJCHUP04Cb9HrW3UPsfOwTGD8E6p2OGKvyVse9wvgLuWkgQpq94UzpIiwAoZTjGo65KgEQLLZBKozfl7tIgV00XUByFHlU',
        'client_secret': 'test client secret'
    }

    return render(request, template, context)
