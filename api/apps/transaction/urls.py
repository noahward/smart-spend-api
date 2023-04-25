from django.urls import path

from .views import (
    TransactionList,
    TransactionDetail,
    TransactionFileUpload,
    preview_transaction_file,
)

transaction_urls = [
    path("api/v1/transactions/", TransactionList.as_view(), name="transaction-list"),
    path(
        "api/v1/transactions/<int:tid>/",
        TransactionDetail.as_view(),
        name="transaction-detail",
    ),
    path(
        "api/v1/transaction-file-preview/",
        preview_transaction_file,
        name="transaction-file-preview",
    ),
    path(
        "api/v1/transaction-file-upload/",
        TransactionFileUpload.as_view(),
        name="transaction-file-upload",
    ),
]
