"""
Root URL configuration for the project.

This file organizes routes into groups:
- Core Django admin
- Authentication (session, JWT, password reset, registration)
- Social authentication (Google)
- Application modules (User, Project)
"""

from django.contrib import admin
from django.urls import path, include
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView
from rest_framework_simplejwt.views import TokenRefreshView

from users.allauth import GoogleLogin, me_google


urlpatterns = [
    # -------------------------
    # Django Admin
    # -------------------------
    path("admin/", admin.site.urls),
    # -------------------------
    # Authentication: Default (dj-rest-auth)
    # -------------------------
    path("auth/", include("dj_rest_auth.urls")),
    # Password reset (customized)
    path("auth/reset-password/", PasswordResetView.as_view(), name="reset-password"),
    path(
        "auth/confirm-reset-password/",
        PasswordResetConfirmView.as_view(),
        name="confirm-reset-password",
    ),
    # Registration
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    # JWT Token refresh
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # -------------------------
    # Social Authentication (Google)
    # -------------------------
    path("auth/google/login/", GoogleLogin.as_view(), name="google_login"),
    path("auth/google/me/", me_google, name="me_google"),
    # -------------------------
    # Application Modules
    # -------------------------
    path("user/", include("users.urls")),
    path("project/", include("project.urls")),
]
