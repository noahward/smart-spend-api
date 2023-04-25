from django.urls import path

from .views import AccountList, AccountDetail

account_urls = [
    path("api/v1/accounts/", AccountList.as_view(), name="accounts-list"),
    path("api/v1/accounts/<int:aid>/", AccountDetail.as_view(), name="accounts-detail"),
]
