from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

from cart.cart import Cart
from shop.models import Product


def cart_view(request):
    cart = Cart(request)
    return render(request, 'cart/cart_view.html', {'cart': cart})


def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        product = get_object_or_404(Product, pk=product_id)
        cart.add(product=product, quantity=product_qty)
        cart_qty = cart.__len__()

        response = JsonResponse({'qty': cart_qty, 'product': product.title})
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product_id, product_qty)
        return HttpResponse(status=200)


def delete_product(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = request.POST.get('product_id')
        product_qty = int(request.POST.get('product_qty'))
        cart.delete(product_id, product_qty)
        return HttpResponse(status=200)
