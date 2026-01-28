from django.urls import path
from .views import ProductsByTagView, AllTagsView, UpdateProductStatusView, AddProductView, ProductDetailView

urlpatterns = [
    path('by-tag/<str:tag_name>/', ProductsByTagView.as_view(), name='products-by-tag'),
    path('tags/', AllTagsView.as_view(), name='all-tags'),
    path('<int:product_id>/status/', UpdateProductStatusView.as_view(), name='update-product-status'),
    path('add/', AddProductView.as_view(), name='add-product'),
    path('<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
]
