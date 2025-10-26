from django.db import models
from django.conf import settings

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

from django.utils.translation import gettext_lazy as _

from common.models import BaseModel
from project.models import Project

from .ruleset import RoleEnum
from .manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_("Date joined"))
    code = models.CharField(
        max_length=128,
        unique=True,
        null=True,
        blank=True,
        verbose_name=_("ID Student"),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        fn = (self.first_name or " ").strip()
        ln = (self.last_name or " ").strip()
        return fn + ln or None


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
