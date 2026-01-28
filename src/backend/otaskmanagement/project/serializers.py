"""DRF data serializers for Project app."""

from otaskmanagement.utils import FormatProjectKey
from rest_framework import serializers

from .models import AccessType, Project, ProjectMembership, RoleEnum


class ProjectSerializer(serializers.ModelSerializer):
    """Serializer for Project."""

    class Meta:
        model = Project
        fields = "__all__"


class ProjectMembershipSerializer(serializers.ModelSerializer):
    # member = UserSerializer()
    # project = ProjectSerializer()

    class Meta:
        model = ProjectMembership
        fields = "__all__"


class WriteProjectMembershipSerializer(serializers.Serializer):
    project = serializers.CharField()
    role = serializers.ChoiceField(choices=RoleEnum.choices, required=False)
    access = serializers.ChoiceField(choices=AccessType.choices, required=False)
    member = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        project_name = validated_data.get("project")
        member_name = validated_data.get("member")
        role_choice = validated_data.get("role", None)
        access_choice = validated_data.get("access", None)

        project_key = FormatProjectKey(project_name)
        project, prj_created = Project.objects.get_or_create(
            key=project_key, defaults={"name": project_name, "access": access_choice}
        )

        defaults = {}
        if role_choice is not None and role_choice != "":
            defaults["role"] = role_choice

        membership, mbs_created = ProjectMembership.objects.get_or_create(
            project=project, member=member_name, defaults=defaults or None
        )

        self._created = mbs_created

        return membership

    def update(self, instance, validated_data):
        project_name = validated_data.get("project", None)
        access_choice = validated_data.get("access", None)

        if project_name is not None:
            project_key = FormatProjectKey(project_name)
            project, _ = Project.objects.get_or_create(
                key=project_key,
                defaults={"name": project_name, "access": access_choice},
            )
            instance.project = project

        role_choice = validated_data.get("role", None)
        if role_choice is not None:
            instance.role = role_choice

        instance.save()
        self._created = False
        return instance
