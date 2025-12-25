from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    direction = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100) 
    isVendor = models.BooleanField(default=False)
    class Meta:
        db_table = "users"

class Tag(models.Model):
    TAG_CHOICES = [
        ("gaming", "Gaming"),
        ("laptop", "Laptop"),
        ("pc", "PC"),
        ("celular", "Celular"),
        ("tablet", "Tablet"),
        ("accesorio", "Accesorio"),
        ("ssd", "SSD"),
        ("ram", "RAM"),
    ]

    name = models.CharField(
        max_length=50,
        choices=TAG_CHOICES,
        unique=True
    )

    def __str__(self):
        return self.get_name_display()

    class Meta:
        db_table = "tags"

class Product(models.Model):
    id_product = models.CharField(max_length = 100)
    name_product = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    tags = models.ManyToManyField(
        Tag,
        related_name="products",
        blank=True
    )
    class Meta:
        db_table = "products"

