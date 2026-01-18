from django.http import JsonResponse
from django.shortcuts import render
import requests
from .models import Cart, CartItem, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from auth_app.models import Product, Tag
from django.db.models import F, Sum
from django.db import transaction

# Create your views here
@api_view(['POST'])
def create_cart(request):
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({"error": "user_id is required"}, status=400)
    
    cart, _ = Cart.objects.get_or_create(user_id=user_id)

    items = [
        {
            "product": item.product.name_product,
            "quantity": item.quantity,
            "price": float(item.price),
            "subtotal": float(item.price * item.quantity),
            "img": item.product.img
        }
        for item in cart.items.all()
    ]

    return JsonResponse({"items": items})

@api_view(['POST'])
def add_to_cart(request):
    user_id = request.data.get("user_id")
    if not user_id:
        return Response({"error": "user_id is required"}, status=400)
    
    product_id = request.data.get("product_id")
    quantity = int(request.data.get("quantity", 1))

    # 1️⃣ Obtener o crear carrito
    cart, _ = Cart.objects.get_or_create(user_id=user_id)

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
                "price": str(cart_item.price),
                "img": product.img
            }
        },
        status=201
    )

@api_view(['GET'])
def get_totalcarro(request):
    user_id = request.query_params.get('user_id')
    if not user_id:
        return Response({"error": "user_id is required"}, status=400)
    
    cart, _ = Cart.objects.get_or_create(user_id=user_id)
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


@api_view(['POST'])
def checkout(request):
    """
    Procesa el carrito y crea una orden de compra.
    POST /api/ventas/checkout/
    Body: { "user_id": 1 }
    """
    user_id = request.data.get('user_id')
    if not user_id:
        return Response({"error": "user_id is required"}, status=400)
    
    # Obtener carrito
    try:
        cart = Cart.objects.get(user_id=user_id)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=404)
    
    cart_items = cart.items.select_related('product', 'product__vendor').all()
    
    if not cart_items.exists():
        return Response({"error": "Cart is empty"}, status=400)
    
    # Calcular total
    total = sum(item.price * item.quantity for item in cart_items)
    
    # Crear orden dentro de una transacción
    with transaction.atomic():
        # Crear la orden
        order = Order.objects.create(
            user_id=user_id,
            total=total,
            status="COMPLETADO"
        )
        
        # Crear los items de la orden agrupados por vendedor
        order_items_data = []
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                vendor=item.product.vendor,
                quantity=item.quantity,
                price=item.price
            )
            order_items_data.append({
                "product_id": item.product.id,
                "product_name": item.product.name_product,
                "img": item.product.img,
                "vendor_id": item.product.vendor.id,
                "vendor_name": item.product.vendor.name,
                "quantity": item.quantity,
                "price": str(item.price),
                "subtotal": str(item.price * item.quantity)
            })
        
        # Vaciar el carrito
        cart.items.all().delete()
    
    return Response({
        "message": "Compra realizada exitosamente",
        "order": {
            "id": order.id,
            "total": str(order.total),
            "status": order.status,
            "created_at": order.created_at.isoformat(),
            "items": order_items_data
        }
    }, status=201)