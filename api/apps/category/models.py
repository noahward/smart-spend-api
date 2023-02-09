from django.db import models

from api.apps.user import User


class Category(models.model):
    name = models.CharField(max_length=100)
    detailed_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "detailed_name"], name="unique_category"
            )
        ]


class UserCategory(models.model):
    name = models.CharField(max_length=100)
    detailed_name = models.CharField(max_length=100)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_categories"
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_id", "name", "detailed_name"], name="unique_user_category"
            )
        ]
