# api/views.py
from allauth.socialaccount.models import SocialAccount, SocialToken
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import CustomUser as User
from ..selectors.user_selector import UserSelector
from ..serializers import UserDetailSerializer, UserSerializer


class UserAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        qs = UserSelector.get_active_non_staff_users_by_project(project_id=project_id)
        return qs


class UserDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            social_account = SocialAccount.objects.filter(
                user=user, provider="google"
            ).first()
            if not social_account:
                return Response({"message": "User not link to Goole"}, 400)

            token = SocialToken.objects.filter(
                account=social_account, app__provider="google"
            ).first()

            data = social_account.extra_data
            if data is None:
                return Response({"message": "Data is empty"}, 400)

            profile = User.objects.filter(user=user).first()
            serializer = UserSerializer(profile)

            return Response(
                {
                    "profile": serializer.data,
                    "all-auth": {
                        "email": data.get("email"),
                        "name": data.get("name"),
                        "picture": data.get("picture"),
                    },
                    "has_access_token": bool(token and token.token),
                },
                200,
            )

        except Exception as e:
            return Response({"message": str(e)}, 500)
