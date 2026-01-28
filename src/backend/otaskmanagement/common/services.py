from datetime import timedelta
from uuid import UUID

from django.conf import settings
from django.core import signing
from django.db import transaction
from django.utils import timezone
from project.models import Project, ProjectMembership
from rest_framework.exceptions import ValidationError
from users.models import CustomUser

from common.models import ProjectInvitation
from common.tasks import send_project_invite_email

INVITE_TOKEN_SALT = "project-invite"


def genarate_user_token(project_id, email: str):
    pay_load = {
        "email": email,
        "project": str(project_id),
        "type": "project_invite",
    }
    from django.core import signing

    token = signing.dumps(pay_load, salt=INVITE_TOKEN_SALT)

    return token


def send_project_invitation(project_id, email, role, user):
    project = Project.objects.get(id=project_id)
    invited_by = CustomUser.objects.get(id=user)

    if ProjectInvitation.objects.filter(
        project=project_id,
        email=email,
        accepted_at__isnull=True,
        expired_at__gt=timezone.now(),
    ).exists():
        raise ValidationError("Invalid Invitation")

    token = genarate_user_token(project_id, email)

    ProjectInvitation.objects.create(
        project=project,
        email=email,
        token=token,
        role=role,
        invited_by=invited_by,
        expired_at=timezone.now() + timedelta(days=7),
    )

    verify_url = f"{settings.BACKEND_BASE_URL}email/invite/verify?token={token}"

    send_project_invite_email.delay(
        to_email=email, verify_url=verify_url, project_name=project.name
    )


def verify_invite_token(token: str, *, max_age_seconds: int = 60 * 60 * 24 * 7):
    try:
        data = signing.loads(
            token,
            salt=INVITE_TOKEN_SALT,
            max_age=max_age_seconds,
        )

    except signing.SignatureExpired:
        raise ValidationError("Invitation token expired")

    except signing.BadSignature:
        raise ValidationError("Invalid invitation token")

    if data.get("type") != "project_invite":
        raise ValidationError("Invalid token type")

    data["project"] = UUID(data["project"])

    return data


def accept_project_invitation(token, user):
    data = verify_invite_token(token)

    project_id = data["project"]
    email = data["email"]

    if user.email.lower() != email.lower():
        raise ValidationError({"email": "Invitation is not for this user"})

    if ProjectMembership.objects.filter(
        project_id=project_id,
        member=user,
    ).exists():
        raise ValidationError({"member": "Already in project"})

    try:
        with transaction.atomic():
            invitation = ProjectInvitation.objects.select_for_update().get(
                token=token,
                accepted_at__isnull=True,
                expired_at__gt=timezone.now(),
            )

            invitation.accepted_at = timezone.now()
            invitation.save(update_fields=["accepted_at"])

            return ProjectMembership.objects.create(
                project_id=project_id,
                member=user,
                role=invitation.role,
            )
    except ProjectInvitation.DoesNotExist:
        raise ValidationError("Invitation not found or expired")
