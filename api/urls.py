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
from knox import views as knox_views
from django.urls import path, include
from django.contrib import admin

from api.apps.user.views import MainUser, LoginView, RegisterView
from api.apps.account.views import AccountList

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("knox.urls")),
    path("auth/register", RegisterView.as_view()),
    path("auth/login", LoginView.as_view()),
    path("auth/logout", knox_views.LogoutView.as_view(), name="knox-logout"),
    path("auth/user", MainUser.as_view()),
    path("accounts", AccountList.as_view()),
]
