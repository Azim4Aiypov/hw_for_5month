from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Shop API",
      default_version='v1',
      description="API documentation",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

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

    path('swagger(<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
