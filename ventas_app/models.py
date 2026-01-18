from django.db import models
from auth_app.models import User
from auth_app.models import Product



# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    fecha_inicio = models.DateTimeField(auto_now_add=True) # tal vez necesario para los recibos
    actualizada_en = models.DateTimeField(auto_now=True) #tal vez necesario para los recibos
    class Meta:
        db_table = "carts"
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2)  # precio al momento

    class Meta:
        db_table = "cart_items"
        unique_together = ("cart", "product")


class Order(models.Model):
    """Orden de compra completada"""
    STATUS_CHOICES = [
        ("PENDIENTE", "Pendiente"),
        ("COMPLETADO", "Completado"),
        ("CANCELADO", "Cancelado"),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="COMPLETADO")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "orders"
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.name}"


class OrderItem(models.Model):
    """Items de una orden"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sold_items")
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = "order_items"