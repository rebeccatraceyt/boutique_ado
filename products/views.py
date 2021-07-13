from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
# Q returns 'or' logic for queries
# Allows search for name AND description
from .models import Product

# Create your views here.


def all_products(request):
    """
        A view to show all products,
        including sorting and search queries
    """

    products = Product.objects.all()
    query = None
    # set query to default (none)

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            # 'or' logic for search query
            queries = Q(
                name__icontains=query
                ) | Q(
                    description__icontains=query
                    )
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
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
