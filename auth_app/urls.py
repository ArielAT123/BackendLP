from django.urls import path
from . import views
urlpatterns = [
    # path('login', views.login, name='login'),
    path('register_client', views.register_client, name='register_client'),
    path('register_vendor', views.register_vendor, name='register_vendor'),
]