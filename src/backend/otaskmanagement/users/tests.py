from django.urls import path
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Serializer for list User"""

    class Meta:
        model = CustomUser
        fields = "__all__"


class TestCelery(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        from users.tasks import get_user

        get_user.delay(user.email)
        serializer = UserSerializer(user)
        return Response({"data": serializer.data}, 200)


api_test_urls = [
    path("test-api/", TestCelery.as_view(), name="api-testing"),
]
