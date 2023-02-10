from django.db import models

from api.apps.user import User


class Account(models.model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")

    def __str__(self):
        return str(self.name)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "user_id"], name="unique_account")
        ]
