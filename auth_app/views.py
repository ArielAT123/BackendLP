from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView

from .models import User, Review
from .serializers import VendorProfileSerializer, ReviewSerializer

# -----------------------------------
# LOGIN // Jordan
# -----------------------------------
# from django.contrib.auth.hashers import check_password
# # En el login
# user = User.objects.get(email=email)
# if check_password(password_ingresada, user.password):
#     # Contraseña correcta
# else:
#     # Contraseña incorrecta

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
    isVendor = True
    
    # Hash de la contraseña antes de guardarla
    hashed_password = make_password(password)
    
    user = User.objects.create(
        email=email, 
        password=hashed_password,  # Guardamos la contraseña hasheada
        name=name,
        direction=direction, 
        phone_number=phone_number, 
        isVendor=isVendor
    )
    return Response({'message': 'Vendor registered successfully'}, status=status.HTTP_201_CREATED)

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
