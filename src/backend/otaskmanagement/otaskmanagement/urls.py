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

urlpatterns = [
    path('admin/', admin.site.urls),
    # dj-rest-auth chuẩn
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("auth/token/refresh/", get_refresh_view().as_view(), name="token_refresh"),

    # Social login (BE-only)
    path("api/auth/google/login/", GoogleLogin.as_view(), name="google_login"),

    # Lấy dữ liệu Google đã lưu
    path("api/me/google/", me_google, name="me_google"),

    # Allauth URLs (nếu muốn test redirect flow qua trình duyệt)
    path("accounts/", include("allauth.urls")),
]
