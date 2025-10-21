from rest_framework import serializers
from .models import Category, Product, Review
from django.db.models import Avg

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product']

    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('stars must be between 1 and 5')
        return value

    def validate_text(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('text must not be empty')
        return value


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'rating']

    def get_rating(self, obj):
        agg = obj.reviews.aggregate(avg=Avg('stars'))
        avg = agg.get('avg')
        return round(avg, 2) if avg is not None else None

    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('title must not be empty')
        return value

    def validate_price(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError('price must be greater than 0')
        return value


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('name must not be empty')
        return value
