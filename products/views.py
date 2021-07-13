from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
# Q returns 'or' logic for queries
# Allows search for name AND description
from .models import Product, Category

# Create your views here.


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
