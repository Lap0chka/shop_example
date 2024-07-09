from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from payment.forms import ShippingForm
from payment.models import ShippingAddress


@login_required(login_url='account:login')
def shipping_view(request):
    try:
        shipping_address = ShippingAddress.objects.get(user=request.user)
    except ShippingAddress.DoesNotExist:
        shipping_address = None

    if request.method == 'POST':
        form = ShippingForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            return redirect('account:dashboard')
    else:
        form = ShippingForm(instance=shipping_address)

    return render(request, 'payment/shipping/shipping.html', {'form': form})
