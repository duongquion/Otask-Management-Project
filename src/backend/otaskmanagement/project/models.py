"""Project database model definitions."""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from otaskmanagement.models import BaseModel
from users.ruleset import RoleEnum


class AccessType(models.TextChoices):
    """Defines access-level options for project visibility."""

    PRIVATE = "private", _("Private")
    LIMITED = "limited", _("Limited")
    OPEN = "open", _("Open")


class Project(BaseModel):
    """Model for Project"""

    name = models.CharField(verbose_name=_("Project name"))
    key = models.CharField(verbose_name=_("Project key"))
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ProjectMembership",
        through_fields=("project", "member"),
        related_name="projects",
    )
    access = models.CharField(
        max_length=10, choices=AccessType.choices, default=AccessType.OPEN
    )

    def __str__(self):
        return f"{self.name} - {self.key}"


class ProjectMembership(BaseModel):
    """Model for ProjectMembership"""

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
    is_accepted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("member", "project"), name="unique_member_project"
            )
        ]

        indexes = [
            models.Index(fields=("project", "role")),
            models.Index(fields=("member",)),
        ]

    def save(self, *args, **kwargs):
        """
        Temporary override for debugging save() calls.
        Prints a marker when the model is saved.
        """

        print("z" * 100)
        return super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"[MEMBER]: {self.member} - [PROJECT]: {self.project} - [ROLE]: {self.role}"
        )
