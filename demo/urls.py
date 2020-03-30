from django.contrib import admin
from django.urls import path,include
from .views import home,checkoutView,ProductView,PaymentView,OrderView
from cart.views import add_to_cart,remove_from_cart,CartView ,decreaseCart
# for builtin views
from django.contrib.auth import views as auth_views

app_name = 'demo'

urlpatterns = [
    path('',home.as_view(),name='demo'),
    path('add/<slug>',add_to_cart,name='cart'),
    path('cart/',CartView,name='cart-home'),
    path('remove/<slug>',remove_from_cart,name='remove'),
    path('decrease-cart/<slug>', decreaseCart, name='decrease-cart'),
    path('product/<slug>',ProductView.as_view(),name='products'),
    path('checkout/',checkoutView.as_view(),name='checkout'),
    path('payment/<payment_option>',PaymentView.as_view(),name='payment'),
    path('orders/',OrderView.as_view(),name='order'),
    ]
