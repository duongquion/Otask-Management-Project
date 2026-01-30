"""Issue database model definitions."""

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from otaskmanagement.models import BaseModel
from project.models import Project


class IssueTypeEnum(models.TextChoices):
    USERSTORY = "userstory", _("User Story")
    BUG = "bug", _("Bug")
    TASK = "task", _("Task")


class PriorityEnum(models.TextChoices):
    HIGH = "high", _("High")
    MEDIUM = "medium", _("Medium")
    LOW = "low", _("Low")


class StateEnum(models.TextChoices):
    COMMITTED = "committed", _("Committed")
    REJECTED = "rejected", _("Rejected")
    APPROVED = "approved", _("Approved")


class Sprint(BaseModel):
    name = models.CharField(max_length=256, verbose_name=_("Sprint Name"))
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="+",
    )
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(verbose_name=_("End Date"))
    is_closed = models.BooleanField(default=False, verbose_name=_("Is Close"))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("name", "project"), name="unique_sprint_project"
            )
        ]

        indexes = [
            models.Index(fields=["project", "is_closed"]),
            models.Index(fields=["project", "start_date"]),
        ]


class IssueStatus(BaseModel):
    """Status: NEW - IN PROGRESS - DONE"""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="+",
    )
    name = models.CharField(unique=True, max_length=180, verbose_name=_("Status Name"))
    is_done = models.BooleanField(default=False)
    order_index = models.IntegerField()
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


# SOON: Write a signals to catch after the project has been created,
# then an issue status will auto create three column constrant (NEW - INPROGRESS - DONE)
"""SIGNALS"""


class Issues(BaseModel):
    key = models.CharField(max_length=108, unique=True, db_index=True)
    title = models.CharField(max_length=208)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    due_date = models.DateField()

    type = models.CharField(
        max_length=10,
        choices=IssueTypeEnum.choices,
        default=IssueTypeEnum.TASK,
    )

    priority = models.CharField(
        max_length=10,
        choices=PriorityEnum.choices,
        null=True,
    )

    state = models.CharField(
        max_length=10,
        choices=StateEnum.choices,
        null=True,
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="+",
    )

    sprint = models.ForeignKey(
        Sprint,
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
    )

    status = models.ForeignKey(
        IssueStatus,
        on_delete=models.SET_NULL,
        related_name="+",
        null=True,
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="sub_issues",
        null=True,
    )

    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="return_assignee",
        null=True,
    )

    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="return_reporter",
        null=True,
    )


class StoryMeta(BaseModel):
    issue = models.OneToOneField(
        Issues,
        on_delete=models.CASCADE,
        limit_choices_to={"type": IssueTypeEnum.USERSTORY},
    )
    story_point = models.IntegerField()


class TaskMeta(BaseModel):
    issue = models.OneToOneField(
        Issues,
        on_delete=models.CASCADE,
        limit_choices_to={"type": IssueTypeEnum.TASK},
    )
    task_point = models.IntegerField()


class BugMeta(BaseModel):
    issue = models.OneToOneField(
        Issues,
        on_delete=models.CASCADE,
        limit_choices_to={"type": IssueTypeEnum.BUG},
    )
    # SOON: Adding other point or other type for bug
