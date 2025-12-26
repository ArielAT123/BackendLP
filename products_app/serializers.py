from rest_framework import serializers
from auth_app.models import Product, Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer para las etiquetas de productos"""
    
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    """Serializer para productos con sus etiquetas"""
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    vendor_name = serializers.CharField(source='vendor.name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id',
            'id_product',
            'name_product',
            'description',
            'price',
            'stock',
            'vendor_name',
            'tags'
        ]
