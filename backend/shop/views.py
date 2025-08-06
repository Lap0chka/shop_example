from django.contrib import messages
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
    if request.method == 'POST':
        if request.user.is_authenticated:
            if product.reviews.filter(created_by=request.user).exists():
                messages.error(
                    request, 'You have already made a review for this product.')
            else:
                rating = request.POST.get('rating', 3)
                content = request.POST.get('content', '')
                if content:
                    product.reviews.create(
                        rating=rating, content=content, created_by=request.user, product=product)
                    return redirect(request.path)
        else:
            messages.error(
                request, 'You need to be logged in to make a review.')

    context = {'product': product}
    return render(request, 'shop/product_detail.html', context)



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
