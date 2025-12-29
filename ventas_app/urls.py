from django.urls import path
from ventas_app.views import get_totalcarro, add_to_cart, create_cart

urlpatterns = [
    path("cart/", create_cart, name="cart-detail"),
    path("cart/add/", add_to_cart, name="cart-add"),
    path("cart/total/", get_totalcarro, name="cart-total"),
]
