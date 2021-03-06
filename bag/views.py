from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product


def view_bag(request):
    """
        A view that renders bag content page
    """
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """
        Add a quantity of the specified product to the shopping bag
    """

    # get the product
    product = get_object_or_404(Product, pk=item_id)

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
                messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
            else:
                # if item is different size, add as new item
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added size {size.upper()} {product.name} to your bag')
    else:
        # if the product has no size
        # object dictionary stores product and quantity
        # if product is already in bag, quantity increments
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    # override varible in session with update
    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """
        Adjust quantity of a specified product
    """
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    # New quantity of product
    if size:
        # if there is a size for product
        if quantity > 0:
            # if quantity is greater than zero
            # set quantity according to adjustment
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {bag[item_id]["items_by_size"][size]}')
        else:
            # otherwise, remove it
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                # if items_by_size dict is empty
                # remove item from bag
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
    else:
        # if there is no size for product
        if quantity > 0:
            # remain the same
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            # remove the product
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """
        Remove the item from the bag
    """

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            # check if product to be deleted has a size
            # if it does, only remove that size, not others
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                # if items_by_size dict is empty
                # remove item from bag
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your bag')
        else:
            # if there is no size for product
            # remove the product
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
