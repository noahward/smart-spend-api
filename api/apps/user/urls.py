from django.urls import path, include

from .views import ActivateUser

user_urls = [
    path(
        "api/v1/auth/users/activate/<uid>/<token>",
        ActivateUser.as_view({"get": "activation"}),
        name="activation",
    ),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("djoser.urls.authtoken")),
]
