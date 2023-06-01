from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ActivateUser, CustomUserViewSet

router = DefaultRouter()
router.register("users", CustomUserViewSet, basename="user")

user_urls = [
    path(
        "api/v1/auth/users/activate/<uid>/<token>",
        ActivateUser.as_view({"get": "activation"}),
        name="activation",
    ),
    path("api/v1/auth/", include(router.urls)),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("djoser.urls.authtoken")),
]
