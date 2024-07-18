

from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView

from .models import Category, Product


class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    paginate_by = 15

    def get_queryset(self):
        return Product.availability.all()

    def get_template_names(self):
        if self.request.htmx:
            return "shop/components/product_list.html"
        return "shop/products.html"


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


def search_products(request):
    query = request.GET['q']
    if not query:
        return redirect('shop:products')
    products = Product.availability.filter(title__icontains=query).distinct()
    context = {'products': products}
    return render(request, 'shop/products.html', context)
