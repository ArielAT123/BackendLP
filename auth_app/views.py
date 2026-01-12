from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView

from .models import User, Review, Store
from .serializers import VendorProfileSerializer, ReviewSerializer

# -----------------------------------
# LOGIN
# -----------------------------------
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {'error': 'Email y password son requeridos'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'error': 'Credenciales inválidas'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Verificar contraseña
    if not check_password(password, user.password):
        return Response(
            {'error': 'Credenciales inválidas'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Construir respuesta según el tipo de usuario
    response_data = {
        'message': 'Login exitoso',
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'is_vendor': user.is_vendor
        }
    }
    
    # Si es vendedor, incluir datos de la tienda
    if user.is_vendor:
        try:
            store = user.store
            response_data['store'] = {
                'id': store.id,
                'name': store.name,
                'description': store.description,
                'logo': store.logo
            }
        except Store.DoesNotExist:
            response_data['store'] = None
    
    return Response(response_data, status=status.HTTP_200_OK)

# -----------------------------------
# REGISTER_CLIENT //Ayman
# -----------------------------------
@api_view(['POST'])
def register_client(request):
    email = request.data.get('email')
    password = request.data.get('password')
    name = request.data.get('name')
    
    user = User.objects.create(
        email=email,
        password=make_password(password),
        name=name
    )
    return Response({'message': 'Client registered successfully'}, status=status.HTTP_201_CREATED)

# -----------------------------------
# VENDOR_REGISTER // Ariel
# -----------------------------------
@api_view(['POST'])
def register_vendor(request):
    email = request.data.get('email')
    password = request.data.get('password')
    name = request.data.get('name')
    direction = request.data.get('direction')
    phone_number = request.data.get('phone_number')
    
    # Datos de la tienda
    store_name = request.data.get('store_name', name)  # Por defecto usa el nombre del vendor
    store_description = request.data.get('store_description', '')
    store_logo = request.data.get('store_logo', None)
    
    # Hash de la contraseña antes de guardarla
    hashed_password = make_password(password)
    
    # Crear el usuario como vendor
    user = User.objects.create(
        email=email, 
        password=hashed_password,
        name=name,
        direction=direction, 
        phone_number=phone_number, 
        is_vendor=True
    )
    
    # Crear la tienda asociada al vendor
    store = Store.objects.create(
        vendor=user,
        name=store_name,
        description=store_description,
        logo=store_logo
    )
    
    return Response({
        'message': 'Vendor registered successfully',
        'vendor_id': user.id,
        'store': {
            'id': store.id,
            'name': store.name,
            'description': store.description,
            'logo': store.logo
        }
    }, status=status.HTTP_201_CREATED)

# -----------------------------------
# VENDOR PROFILE
# -----------------------------------
class VendorProfileView(APIView):
    """
    Muestra el perfil público de un vendedor, incluyendo datos básicos.
    """
    def get(self, request, vendor_id):
        try:
            vendor = User.objects.get(id=vendor_id, is_vendor=True)
        except User.DoesNotExist:
            return Response({"error": "Vendedor no encontrado"}, status=404)

        profile_data = {
            "id": vendor.id,
            "name": vendor.name,
            "email": vendor.email,
            "direction": getattr(vendor, "direction", ""),
            "phone_number": getattr(vendor, "phone_number", ""),
            "average_rating": None,  # No calculamos estrellas aún
            "reviews": []  # Lista vacía por ahora
        }

        return Response(profile_data)
