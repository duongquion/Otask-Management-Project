from django.db import models
from django.utils.translation import gettext_lazy as _


class RoleEnum(models.TextChoices):
    ADMINISTRATOR = "administrator", _("Administrator")
    MEMBER = "member", _("Member")
    VIEWER = "viewer", _("Viewer")


RULE_OPTION = ["can_view", "can_edit", "can_add", "can_delete"]
