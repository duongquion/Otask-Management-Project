"""
URL configuration for otaskmanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from users.allauth import GoogleLogin
from users.api import me_google
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.views import PasswordChangeView, PasswordResetConfirmView, PasswordResetView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth with defaut
    path("auth/", include("dj_rest_auth.urls")),
    
    # password/reset/?$,
    path("auth/reset-password/", PasswordResetView.as_view(), name="reset-password"),
    # password/reset/confirm/?$
    path("auth/confirm-reset-password/", PasswordResetConfirmView.as_view(), name="confirm-reset-password"),
    
    # login/?$
    # # URLs that require a user to be logged in with a valid session / token.
    # logout/?$
    # user/?$
    # password/change/?$
    
    path("auth/registration/", include('dj_rest_auth.registration.urls')),
    path("auht/token/refresh/", get_refresh_view().as_view(), name="token_refresh"),

    # Auth with social media
    path("api/auth/google/login/", GoogleLogin.as_view(), name="google_login"),
    path("api/me/google/", me_google, name="me_google"),
]
