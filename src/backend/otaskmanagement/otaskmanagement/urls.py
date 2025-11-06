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
