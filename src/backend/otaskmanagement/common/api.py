from django.core.mail import send_mail
from rest_framework import serializers, permissions
from django.conf import settings
from rest_framework.views import APIView, Response

from common.serializers import TestEmailSerializer


class TestEmail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TestEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        delivered = send_mail(
            subject="Test email from OTask",
            message="This is a test email from OTask.",
            recipient_list=[email],
            from_email=settings.EMAIL_HOST_USER,
        )

        if delivered == 0:
            raise serializers.ValidationError("Failed to send test email")

        return Response({"status": "ok"})
