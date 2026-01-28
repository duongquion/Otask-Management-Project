from project.models import ProjectMembership
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView, Response

from common.serializers import EmailSerializer
from common.services import (
    accept_project_invitation,
    send_project_invitation,
    verify_invite_token,
)


class SendEmailMember(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            project_id = self.kwargs["pk"]

            serializer = EmailSerializer(
                data=request.data, context={"project_id": project_id}
            )
            serializer.is_valid(raise_exception=True)

            send_project_invitation(
                project_id=project_id,
                email=serializer.validated_data["email"],
                role=serializer.validated_data["role"],
                user=request.user.id,
            )

            return Response(
                {
                    "detail": (
                        "Request received. The email should arrive in a few minutes."
                    )
                },
                status=200,
            )

        except Exception as e:
            return Response({"Message": str(e)}, status=500)


class VerifyInvitation(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        token = request.query_params.get("token")
        if not token:
            return Response({"status": "INVALID"}, status=400)

        try:
            data = verify_invite_token(token)
        except ValidationError as e:
            return Response({"status": "INVALID", "message": str(e)}, status=400)

        if not request.user.is_authenticated:
            return Response({"status": "NEED_AUTH"}, status=401)

        if ProjectMembership.objects.filter(
            project_id=data["project"],
            member=request.user,
        ).exists():
            return Response({"status": "ALREADY_MEMBER"}, status=200)

        return Response({"status": "READY"}, status=200)


class AcceptInvitation(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        token = request.data.get("token")
        if not token:
            raise ValidationError({"token": "Required"})

        membership = accept_project_invitation(token, request.user)

        return Response(
            {
                "message": "Succesfully",
                "project": membership.project,
            },
            status=201,
        )
