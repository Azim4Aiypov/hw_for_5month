from rest_framework import generics, permissions
from django.db.models import Avg, Count
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.annotate(products_count=Count('products'))
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.annotate(products_count=Count('products'))
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all().annotate(rating=Avg('reviews__stars'))
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().annotate(rating=Avg('reviews__stars'))
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductReviewsListView(generics.ListAPIView):
    queryset = Product.objects.all().annotate(rating=Avg('reviews__stars'))
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
