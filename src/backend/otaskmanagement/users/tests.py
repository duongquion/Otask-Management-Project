from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import path
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import CustomUser

# class TestPermissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Permission
#         fields = "__all__"

# class TestPermissionAPI(APIView):
#     def get(self, request, *args, **kwargs):
#         content_type = ContentType.objects.filter(app_label__in=settings.PROJECT_APP_LABELS)
#         permission = Permission.objects.filter(content_type__in=content_type)

#         serializer = TestPermissionSerializer(permission, many=True)
#         return Response({"DATA": serializer.data},200)


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
