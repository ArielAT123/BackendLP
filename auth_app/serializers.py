from rest_framework import serializers
from .models import User, Review

# Serializer para Review
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "vendor", "user", "rating", "comment", "created_at"]

# Serializer para mostrar perfil público de un vendedor con sus reseñas
class VendorProfileSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)  # relación reversa de 'vendor'

    class Meta:
        model = User
        fields = ["id", "name", "email", "direction", "phone_number", "reviews"]
