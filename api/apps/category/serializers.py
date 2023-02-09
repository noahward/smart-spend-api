from rest_framework import serializers

from .models import Category, UserCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "detailed_name"]


class UserCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCategory
        fields = ["name", "detailed_name", "user_id"]
