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