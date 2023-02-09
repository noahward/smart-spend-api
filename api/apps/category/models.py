from django.db import models


class Category(models.model):
    name = models.CharField(max_length=100, unique=True)
    detailed_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)
