from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from auth_app.models import Product, Tag
from .serializers import ProductSerializer, CreateProductSerializer
from .serializers import ProductStatusSerializer


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

class UpdateProductStatusView(APIView):
    """
    Permite al vendedor actualizar el estado de su publicación.
    GET /api/products/<int:product_id>/status/
    PATCH /api/products/<int:product_id>/status/
    """
    # permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        """
        Muestra el producto y su estado actual (habilita la Browsable API)
        """
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Producto no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductStatusSerializer(product)
        return Response(serializer.data)

    def patch(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Producto no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )


        serializer = ProductStatusSerializer(
            product,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Estado de la publicación actualizado correctamente",
                    "product_id": product.id,
                    "new_status": serializer.data["status"]
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddProductView(APIView):
    """
    Vista para agregar un nuevo producto asociado a un vendedor.
    POST /api/products/add/
    
    Body esperado:
    {
        "id_product": "PROD-001",
        "name_product": "Laptop Gaming",
        "description": "Laptop para gaming",
        "price": 1500.00,
        "stock": 10,
        "vendor_id": 1,
        "tags": ["gaming", "laptop"]  // opcional
    }
    """
    
    def post(self, request):
        serializer = CreateProductSerializer(data=request.data)
        
        if serializer.is_valid():
            product = serializer.save()
            return Response({
                "message": "Producto creado exitosamente",
                "product": {
                    "id": product.id,
                    "id_product": product.id_product,
                    "name_product": product.name_product,
                    "price": str(product.price),
                    "stock": product.stock,
                    "img": product.img,
                    "vendor": product.vendor.name,
                    "tags": [tag.name for tag in product.tags.all()]
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    """
    Vista para obtener los detalles de un producto por su ID.
    GET /api/products/<int:product_id>/
    """

    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Producto no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
