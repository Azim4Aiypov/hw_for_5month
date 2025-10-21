from django.urls import path
from .views import (
    CategoryListCreateView, CategoryRetrieveUpdateDestroyView,
    ProductListCreateView, ProductRetrieveUpdateDestroyView,
    ProductReviewsListView,
    ReviewListCreateView, ReviewRetrieveUpdateDestroyView
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),

    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),

    path('products/reviews/', ProductReviewsListView.as_view(), name='product-reviews-list'),

    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewRetrieveUpdateDestroyView.as_view(), name='review-detail'),
]
