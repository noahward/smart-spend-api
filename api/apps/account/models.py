from django.db import models

from api.apps.user.models import User


class Account(models.Model):
    kind_choices = (("spending", "spending"), ("saving", "saving"))

    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, null=True, blank=True)
    kind = models.CharField(max_length=100, choices=kind_choices)
    amount = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")

    def __str__(self):
        return str(self.name)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "user"], name="unique_account")
        ]
