from ..models import CustomUser as User


class UserSelector:
    @staticmethod
    def _base_selector():
        return User.objects.filter(
            is_active=True,
            is_staff=False,
        )

    @classmethod
    def get_active_non_staff_users_by_project(cls, project_id: str):
        return cls._base_selector().filter(projects__pk=project_id).distinct()
