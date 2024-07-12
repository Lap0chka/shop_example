from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('shipping/', views.shipping_view, name='register'),
    path('payment-failed/', views.payment_failed, name='payment_failed'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('complete_order/', views.complete_order, name='complete_order'),
    path('checkout/', views.checkout, name='checkout'),

]
