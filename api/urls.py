from django.urls import path
from django.contrib import admin

from api.apps.user.urls import user_urls
from api.apps.account.urls import account_urls
from api.apps.category.urls import category_urls
from api.apps.transaction.urls import transaction_urls

urlpatterns = [
    path("admin/", admin.site.urls),
]

urlpatterns += user_urls
urlpatterns += account_urls
urlpatterns += category_urls
urlpatterns += transaction_urls
