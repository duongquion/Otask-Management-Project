from django.db import models
from django.conf import settings
from otaskmanagement.models import BaseModel
from project.models import Project
from users.ruleset import RoleEnum
from django.db.models import Q


class ProjectInvitation(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="invitations",
    )
    email = models.EmailField()
    role = models.CharField(
        max_length=15,
        choices=RoleEnum.choices,
        default=RoleEnum.MEMBER,
    )
    token = models.CharField(max_length=255, unique=True)
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_invitations",
    )
    expired_at = models.DateTimeField()
    accepted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["token"]),
            models.Index(fields=["email"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["project", "email"],
                condition=Q(accepted_at__isnull=True),
                name="unique_pending_invitation_per_project",
            )
        ]
