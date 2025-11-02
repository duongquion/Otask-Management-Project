# auth/views.py

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

    def post(self, request, *args, **kwargs):
        resp = super().post(request, *args, **kwargs)

        user = self.request.user

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        google = SocialAccount.objects.filter(user=user, provider="google").first()
        extra = google.extra_data if google else None

        data = {
            "access": str(access),
            "refresh": str(refresh),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "firstname": user.first_name,
                "lastname": user.last_name,
            },
            "google_profile": {
                "email": extra.get("email"),
                "name": extra.get("name"),
                "picture": extra.get("picture"),
            }
        }

        return Response(data, status=resp.status_code)
