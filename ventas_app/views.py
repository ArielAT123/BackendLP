from django.http import JsonResponse
from django.shortcuts import render
import requests
from .models import Cart, CartItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from auth_app.models import Product, Tag
from django.db.models import F, Sum

# Create your views here
@api_view(['POST'])
def create_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    items = [
        {
            "product": item.product.name_product,
            "quantity": item.quantity,
            "price": float(item.price),
            "subtotal": float(item.price * item.quantity)
        }
        for item in cart.items.all()
    ]

    return JsonResponse({"items": items})

def add_to_cart(request):
    user = request.user
    product_id = request.data.get("product_id")
    quantity = int(request.data.get("quantity", 1))

    # 1️⃣ Obtener o crear carrito
    cart, _ = Cart.objects.get_or_create(user=user)

    # 2️⃣ Obtener producto
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"},
            status= 404
        )

    # 3️⃣ Verificar stock
    if quantity > product.stock:
        return Response(
            {"error": "Not enough stock"},
            status= 400
        )

    # 4️⃣ Crear o actualizar CartItem
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={
            "quantity": quantity,
            "price": product.price
        }
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return Response(
        {
            "message": "Product added to cart",
            "cart_item": {
                "product": product.name_product,
                "quantity": cart_item.quantity,
                "price": str(cart_item.price)
            }
        },
        status=201
    )

@api_view(['GET'])
def get_totalcarro(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    total = sum(item.price * item.quantity for item in cart.items.all())
    return JsonResponse({"total": float(total)})

def get_total(cart_id):
    total = (
        CartItem.objects
        .filter(cart_id=cart_id)
        .aggregate(total=Sum(F("price") * F("quantity")))
        .get("total") or 0
    )
    return total