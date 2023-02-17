from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Category
        fields = ["name", "detailed_name", "user"]
