from django.db import models

from api.apps.user.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    detailed_name = models.CharField(max_length=100)
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="user_categories",
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Categories"
        # TODO: Ensure a user can't create a category that an admin has created. E.g. when user=null
        constraints = [
            models.UniqueConstraint(
                fields=["name", "detailed_name"], name="unique_category"
            )
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name", "detailed_name"], name="unique_user_category"
            )
        ]
