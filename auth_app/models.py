from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    is_vendor = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "users"

class Store(models.Model):
    """
    Modelo de tienda asociado a un vendedor.
    Cada vendedor tiene una única tienda.
    """
    vendor = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
        related_name="store",
        limit_choices_to={"is_vendor": True}
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    logo = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "stores"

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

    STATUS_CHOICES = [
        ("ACTIVO", "Activo"),
        ("PAUSADO", "Pausado"),
        ("VENDIDO", "Vendido"),
    ]

    id_product = models.CharField(max_length=100, unique=True)
    name_product = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="ACTIVO"
    )

    vendor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="vendor_id",
        related_name="products"
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="products",
        blank=True
    )

    class Meta:
        db_table = "products"

class Review(models.Model):
    vendor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        limit_choices_to={"is_vendor": True}
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="given_reviews"
    )
    rating = models.PositiveSmallIntegerField()  # 1 a 5
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} - {self.vendor.name}"




