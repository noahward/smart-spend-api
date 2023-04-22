"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin

from api.apps.user.urls import user_urls
from api.apps.account.views import AccountList, AccountDetail
from api.apps.category.views import CategoryList, CategoryDetail
from api.apps.transaction.views import (
    TransactionList,
    TransactionDetail,
    TransactionFileUpload,
    preview_transaction_file,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts", AccountList.as_view(), name="accounts"),
    path("accounts/<int:aid>", AccountDetail.as_view(), name="account"),
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
    path("categories", CategoryList.as_view(), name="categories"),
    path("categories/<int:cid>", CategoryDetail.as_view(), name="category"),
]

urlpatterns += user_urls
