from django.db import models

import api.apps.transaction.models as transaction_models
from api.apps.user.models import User


class Account(models.Model):
    kind_choices = (("spending", "spending"), ("saving", "saving"))

    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=100, choices=kind_choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    initial_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    @property
    def balance(self):
        transactions = transaction_models.Transaction.objects.filter(account=self.id)
        balance = self.initial_balance
        for transaction in transactions:
            balance += transaction.amount
        return balance

    def __str__(self):
        return str(self.name)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "user"], name="unique_account")
        ]
