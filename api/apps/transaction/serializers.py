from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Transaction


class BulkCreateListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        result = [self.child.create(attrs) for attrs in validated_data]

        try:
            self.child.Meta.model.objects.bulk_create(result)
        except IntegrityError as e:
            raise ValidationError(e)

        return result


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name")
    category_detailed_name = serializers.CharField(source="category.detailed_name")

    def create(self, validated_data):
        instance = Transaction(**validated_data)

        if isinstance(self._kwargs["data"], dict):
            instance.save()

        return instance

    class Meta:
        model = Transaction
        fields = [
            "id",
            "date",
            "description",
            "currency_code",
            "amount",
            "date_classified",
            "user",
            "account",
            "category_name",
            "category_detailed_name",
        ]
        list_serializer_class = BulkCreateListSerializer
