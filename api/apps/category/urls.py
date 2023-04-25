from django.urls import path

from .views import CategoryList, CategoryDetail

category_urls = [
    path("api/v1/categories/", CategoryList.as_view(), name="category-list"),
    path(
        "api/v1/categories/<int:cid>/", CategoryDetail.as_view(), name="category-detail"
    ),
]
