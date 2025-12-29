from django.contrib import admin
from .models import User, Product, Tag, Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name_product",
        "price",
        "status",
        "vendor",
    )
    list_filter = ("status", "tags")
    search_fields = ("name_product", "vendor__name")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "is_vendor")
    search_fields = ("name", "email")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "vendor",
        "user",
        "rating",
        "created_at",
    )
    list_filter = ("rating",)
    search_fields = ("vendor__name", "user__name")
