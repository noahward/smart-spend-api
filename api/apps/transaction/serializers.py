from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
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
            "account",
            "account_name",
            "category",
            "category_name",
        ]
