from django.urls import path
from django.contrib import admin

from api.apps.user.urls import user_urls
from api.apps.account.urls import account_urls
from api.apps.category.views import category_urls
from api.apps.transaction.views import (
    TransactionList,
    TransactionDetail,
    TransactionFileUpload,
    preview_transaction_file,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("transactions", TransactionList.as_view(), name="transactions"),
    path(
        "transaction-file-preview",
        preview_transaction_file,
        name="transaction-file-preview",
    ),
    path(
        "transaction-file-upload",
        TransactionFileUpload.as_view(),
        name="transaction-file-upload",
    ),
    path("transactions/<int:tid>", TransactionDetail.as_view(), name="transaction"),
]

urlpatterns += user_urls
urlpatterns += account_urls
urlpatterns += category_urls
