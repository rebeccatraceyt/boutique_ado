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

    # check if product has size
    # default is 'no size'
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']

    bag = request.session.get('bag', {})
    # stores 'bag' session (what user saves in bag)
    # checks for bag variable in session
    # if not, one is created

    # checks if product added to bag has size
    # by size, to allow one item and multiple sizes
    if size:
        # IS already in bag
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                # if item is same size, increment quantity
                bag[item_id]['items_by_size'][size] += quantity
            else:
                # if item is different size, add as new item
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        # if the product has no size
        # object dictionary stores product and quantity
        # if product is already in bag, quantity increments
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    # override varible in session with update
    request.session['bag'] = bag
    return redirect(redirect_url)
