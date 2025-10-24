from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def home(request):
    return JsonResponse({"message": "Welcome to Shop API!"})


def api_home(request):
    return JsonResponse({"message": "API is working"})

urlpatterns = [
    path('', home), 
    path('admin/', admin.site.urls), 
    path('api/v1/users/', include('users.urls')), 
    path('api/v1/products/', include('product.urls')),  
    path('api/v1/', api_home), 
]
