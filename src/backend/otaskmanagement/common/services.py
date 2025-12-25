from uuid import UUID
from datetime import timedelta

from django.core import signing
from django.utils import timezone
from django.conf import settings
from django.db import transaction
from django.template.loader import render_to_string

from rest_framework.exceptions import ValidationError

from common.models import ProjectInvitation
from project.models import Project, ProjectMembership

INVITE_TOKEN_SALT = "project-invite"


def genarate_user_token(project_id, email: str):

    pay_load = {
        "email": email,
        "project": str(project_id),
        "type": "project_invite",
    }

    token = signing.dumps(pay_load, salt=INVITE_TOKEN_SALT)

    return token


def send_project_invite_email(to_email, verify_url, project_name):
    subject = f"You've been invited to join project {project_name}"

    text_content = (
        f"You have been invited to join project {project_name}.\n"
        f"Open this link to accept:\n{verify_url}"
    )

    html_content = render_to_string(
        "email/project_invite.html",
        {
            "project_name": project_name,
            "verify_url": verify_url,
        },
    )

    from django.core.mail import EmailMultiAlternatives

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )

    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)


def send_project_invitation(project_id, email, role, invited_by):

    project = Project.objects.get(id=project_id)

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

    verify_url = f"{settings.LOCAL_DOMAIN}email/invite/verify?token={token}"

    send_project_invite_email(
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
