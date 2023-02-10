from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "date",
            "description",
            "currency",
            "amount",
            "user_id",
            "account_id",
            "category_id",
            "user_category_id",
        ]
