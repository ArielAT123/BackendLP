from django.urls import path
from .views import ProductsByTagView, AllTagsView

urlpatterns = [
    path('by-tag/<str:tag_name>/', ProductsByTagView.as_view(), name='products-by-tag'),
    path('tags/', AllTagsView.as_view(), name='all-tags'),
]
