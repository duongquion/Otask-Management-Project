from django.db import models
from common.models import BaseModel
from django.utils.translation import gettext_lazy as _


class Project(BaseModel):
    name = models.CharField(verbose_name=_("Project name"))
    key = models.CharField(verbose_name=_("Project key"))
