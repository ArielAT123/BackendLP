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
            'img',
            'vendor_name',
            'tags'
        ]

class ProductStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['status']


class CreateProductSerializer(serializers.ModelSerializer):
    """Serializer para crear productos"""
    vendor_id = serializers.IntegerField(write_only=True)
    tags = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Product
        fields = [
            'id_product',
            'name_product',
            'description',
            'price',
            'stock',
            'img',
            'vendor_id',
            'tags'
        ]
    
    def validate_vendor_id(self, value):
        from auth_app.models import User
        try:
            user = User.objects.get(id=value)
            if not user.is_vendor:
                raise serializers.ValidationError("El usuario no es un vendedor")
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("El vendedor no existe")
    
    def create(self, validated_data):
        from auth_app.models import User
        vendor_id = validated_data.pop('vendor_id')
        tags_data = validated_data.pop('tags', [])
        
        vendor = User.objects.get(id=vendor_id)
        product = Product.objects.create(vendor=vendor, **validated_data)
        
        # Agregar tags si existen
        for tag_name in tags_data:
            try:
                tag = Tag.objects.get(name=tag_name.lower())
                product.tags.add(tag)
            except Tag.DoesNotExist:
                pass  # Ignorar tags que no existen
        
        return product