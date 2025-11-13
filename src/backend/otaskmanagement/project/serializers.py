from rest_framework import serializers
from django.db import transaction, IntegrityError

from .models import Project, ProjectMembership, RoleEnum, AccessType
from users.serializers import UserSerializer
from otaskmanagement.utils import FormatProjectKey

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ["id"]


class ProjectMembershipSerializer(serializers.ModelSerializer):
    member =  UserSerializer()
    project = ProjectSerializer()
    
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
        project, prj_created = Project.objects.get_or_create(key=project_key, defaults={"name":project_name})
        
        defaults = {}
        if role_choice is not None and role_choice != "":
            defaults["role"] = role_choice
        if access_choice is not None and access_choice != "":
            defaults["access"] = access_choice
            
        membership, mbs_created = ProjectMembership.objects.get_or_create(
                    project=project,
                    member=member_name,
                    defaults=defaults or None
                )
        
        self._created = mbs_created
                
        return membership
    
    def update(self, instance, validated_data):

        project_name = validated_data.get("project", None)
        if project_name is not None:
            project_key = FormatProjectKey(project_name)
            project, _ = Project.objects.get_or_create(
                key=project_key,
                defaults={"name": project_name},
            )
            instance.project = project

        role_choice = validated_data.get("role", None)
        if role_choice is not None:
            instance.role = role_choice

        access_choice = validated_data.get("access", None)
        if access_choice is not None:
            instance.access = access_choice

        instance.save()
        self._created = False
        return instance