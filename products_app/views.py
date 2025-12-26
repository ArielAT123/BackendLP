from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from auth_app.models import Product, Tag
from .serializers import ProductSerializer


class ProductsByTagView(APIView):
    """
    Vista para obtener todos los productos que tienen una etiqueta en común.
    GET /api/products/by-tag/<tag_name>/
    """
    
    def get(self, request, tag_name):
        # Validar que la etiqueta existe
        try:
            tag = Tag.objects.get(name=tag_name.lower())
        except Tag.DoesNotExist:
            # Obtener lista de etiquetas válidas
            valid_tags = [choice[0] for choice in Tag.TAG_CHOICES]
            return Response(
                {
                    "error": f"La etiqueta '{tag_name}' no existe.",
                    "valid_tags": valid_tags
                },
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Obtener productos con esa etiqueta
        products = Product.objects.filter(tags=tag).select_related('vendor')
        serializer = ProductSerializer(products, many=True)
        
        return Response({
            "tag": tag_name,
            "count": products.count(),
            "products": serializer.data
        })


class AllTagsView(APIView):
    """
    Vista para obtener todas las etiquetas disponibles.
    GET /api/products/tags/
    """
    
    def get(self, request):
        tags = [{"value": choice[0], "label": choice[1]} for choice in Tag.TAG_CHOICES]
        return Response({
            "count": len(tags),
            "tags": tags
        })
