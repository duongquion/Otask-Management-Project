# api/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from allauth.socialaccount.models import SocialAccount, SocialToken

from .serializers import UserSerializer
from .models import CustomUser as User

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_google(request):
    acc = SocialAccount.objects.filter(user=request.user, provider="google").first()
    if not acc:
        return Response({"detail": "User chưa liên kết Google"}, status=404)
    profile = acc.extra_data or {}
    token = SocialToken.objects.filter(account=acc, app__provider="google").first()
    return Response({
        "profile": {
            "email": profile.get("email"),
            "name": profile.get("name"),
            "picture": profile.get("picture"),
        },
        "has_access_token": bool(token and token.token),
    })
    
    
class UserAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
