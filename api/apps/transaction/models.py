from django.db import models

from api.apps.user import User
from api.apps.account import Account
from api.apps.category import Category


class Transaction(models.model):
    date = models.DateField()
    description = models.CharField(max_length=255)
    currency = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
