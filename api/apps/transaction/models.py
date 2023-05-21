from django.db import models

from api.apps.user.models import User
from api.apps.account.models import Account
from api.apps.category.models import Category


class Transaction(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255)
    currency_code = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date_classified = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="transactions"
    )
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="transactions"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="transactions",
    )

    @property
    def account_name(self):
        return self.account.name

    @property
    def category_name(self):
        return self.category.name

    def __str__(self):
        return str(self.id)
