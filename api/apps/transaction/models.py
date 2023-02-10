from django.db import models

from api.apps.user.models import User
from api.apps.account.models import Account
from api.apps.category.models import Category, UserCategory


class Transaction(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=255)
    currency_code = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    category_id = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
    user_category_id = models.ForeignKey(
        UserCategory, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return str(self.id)
