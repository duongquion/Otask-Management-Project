from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from users.models import RolePermission, RoleEnum


def seed_role_permissions(sender, **kwargs):
    content_type = ContentType.objects.filter(app_label__in=settings.PROJECT_APP_LABELS)
    permission = Permission.objects.filter(content_type__in=content_type)

    mapping = {
        RoleEnum.ADMINISTRATOR: permission,
        RoleEnum.MEMBER: permission.filter(codename__endswith="issues"),
        RoleEnum.VIEWER: permission.filter(codename__startswith="view_"),
    }

    for role, perms in mapping.items():
        for perm in perms:
            RolePermission.objects.get_or_create(
                role=role,
                permission=perm,
            )
