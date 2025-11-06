from django.conf import settings

from django.db import models
from otaskmanagement.models import BaseModel
from django.utils.translation import gettext_lazy as _
from users.ruleset import RoleEnum


class Project(BaseModel):
    name = models.CharField(verbose_name=_("Project name"))
    key = models.CharField(verbose_name=_("Project key"))
    

class ProjectMembership(BaseModel):
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships",
        verbose_name=_("Member"),
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="project_memberships",
        verbose_name=_("Project"),
    )
    role = models.CharField(
        max_length=32, choices=RoleEnum.choices, default=RoleEnum.ADMINISTRATOR
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("member", "project"), name="uq_member_project"
            )
        ]

        indexes = [
            models.Index(fields=("project", "role")),
            models.Index(fields=("member",)),
        ]

    def __str__(self):
        return self.member - self.project