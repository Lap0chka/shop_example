from django.urls import path

from shop import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:slug>', views.product_detail, name='product_detail'),
    path('search/<slug:slug>', views.category_list, name='category_list')
]


