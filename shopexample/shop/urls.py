from django.urls import path

from shop import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='products'),
    path('<slug:slug>', views.product_detail, name='product_detail'),
    path('search/<slug:slug>', views.category_list, name='category_list')
]


