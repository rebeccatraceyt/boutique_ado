from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models.functions import Lower
from django.db.models import Q
# Q returns 'or' logic for queries
# Allows search for name AND description

from .models import Product, Category
from .forms import ProductForm


def all_products(request):
    """
        A view to show all products,
        including sorting and search queries
    """

    products = Product.objects.all()

    # set to default (none)
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey

            # sortkey preserves original field 'name'
            if sortkey == 'name':
                # if user is sorting by name
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if sortkey == 'category':
                # if user is sorting by category
                sortkey = 'category__name'

            if 'direction' in request.GET:
                # if user is sorting in decending
                direction = request.GET['direction']

                # decending = '-'
                if direction == 'desc':
                    sortkey = f'-{sortkey}'

            # actually sort the product
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            # 'or' logic for search query
            # 'icontains' specific class contains query
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    # return current sorting method to template
    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)
    # context returns things back to template


def product_detail(request, product_id):
    """
        A view to show individual product details
    """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_details.html', context)
    # context returns things back to template


def add_product(request):
    """
    Add a product to the store
    """
    if request.method == 'POST':
        # instantiate a new instance of the form
        # to capture the image, if one is added
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product \
                Please ensure all fields are valid')
    else:
        # ensures form errors aren't wiped out
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def edit_product(request, product_id):
    """
    Edit a product in the store
    """

    # get the product
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        # instantiate form with specified instance being product chosen
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. \
                Please ensure all fields are vaild')
    else:
        # instantiating the product form (using the product)
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)
