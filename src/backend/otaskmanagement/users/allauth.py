"""
Handles Google OAuth2 authentication using Django Allauth and dj-rest-auth.
"""

from allauth.socialaccount.models import SocialAccount, SocialToken
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


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
            },
        }

        return Response(data, status=resp.status_code)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_google(request):
    acc = SocialAccount.objects.filter(user=request.user, provider="google").first()
    if not acc:
        return Response({"detail": "User chưa liên kết Google"}, status=404)
    profile = acc.extra_data or {}
    token = SocialToken.objects.filter(account=acc, app__provider="google").first()
    return Response(
        {
            "profile": {
                "email": profile.get("email"),
                "name": profile.get("name"),
                "picture": profile.get("picture"),
            },
            "has_access_token": bool(token and token.token),
        }
    )
