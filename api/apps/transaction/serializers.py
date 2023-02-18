from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "date",
            "description",
            "currency_code",
            "amount",
            "user",
            "account",
            "category",
        ]
