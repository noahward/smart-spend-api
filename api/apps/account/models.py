from django.db import models

from api.apps.user import User


class Account(models.model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
