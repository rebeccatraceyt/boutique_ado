from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order


def profile(request):
    """ Display user profile """
    profile = get_object_or_404(UserProfile, user=request.user)

    # if user changes information on profile page:
    if request.method == 'POST':
        # create new instance of the user profile form using post data
        form = UserProfileForm(request.POST, instance=profile)

        # checks if form is valid
        if form.is_valid():
            # valid = save and send success message
            form.save()
            messages.success(request, 'Profile updated successfully')

    form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)


def order_history(request, order_number):
    # get past orders
    order = get_object_or_404(Order, order_number=order_number)

    # informative message on previous orders
    messages.info(request, (
        f'This a past order confirmation for order number {order_number}.'
        'A confirmation email was sent on the order date.'
    ))

    # use checkout success template for rendering order confirmation
    template = 'checkout/checkout_success.html'
    
    context = {
        'order': order,
        # check if user got there from Order History
        'from_profile': True,
    }

    return render(request, template, context)
