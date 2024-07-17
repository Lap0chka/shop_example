from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def index(request):
    """
    View to display the index page with a list of available products.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object with the rendered template and products context.
    """
    products = Product.availability.all()
    return render(request, 'shop/products.html', {'products': products})


def product_detail(request, slug):
    """
    View to display the details of a specific product.
    """
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})


def category_list(request, slug):
    """
    View to display the products in a specific category.
    """
    category = get_object_or_404(Category, slug=slug)
    products = Product.availability.filter(category=category)
    context = {'category': category, 'products': products}
    return render(request, 'shop/category_list.html', context)

