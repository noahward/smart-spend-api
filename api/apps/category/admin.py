from django.contrib import admin

from .models import Category, UserCategory

admin.site.register([Category, UserCategory])
