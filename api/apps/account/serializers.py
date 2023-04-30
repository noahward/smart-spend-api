from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    balance = serializers.ReadOnlyField()

    class Meta:
        model = Account
        fields = ["id", "name", "kind", "currency_code", "balance", "initial_balance"]
