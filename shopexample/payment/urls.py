from django.urls import path

from . import views

app_name = 'payment'

urlpatterns = [
    path('shipping/', views.shipping_view, name='register'),
]
