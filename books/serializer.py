from rest_framework import serializers
from .models import Book
from categories.models import Category

class BookSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True
    )
    class Meta:
        model = Book
        fields = '__all__'