from django.shortcuts import render, redirect


def view_bag(request):
    """
        A view that renders bag content page
    """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """
        Add a quantity of the specified product to the shopping bag
    """

    quantity = int(request.POST.get('quantity'))
    # int converts to integer (from string)

    redirect_url = request.POST.get('redirect_url')
    # know where to redirect when process is finished

    bag = request.session.get('bag', {})
    # stores 'bag' session (what user saves in bag)
    # checks for bag variable in session
    # if not, one is created

    # object dictionary stores product and quantity
    # if product is already in bag, quantity increments
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    # override varible in session with update
    request.session['bag'] = bag
    return redirect(redirect_url)
