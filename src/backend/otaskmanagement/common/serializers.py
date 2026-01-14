from rest_framework import serializers
from common.models import ProjectInvitation
from users.ruleset import RoleEnum


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    role = serializers.ChoiceField(choices=RoleEnum.choices, required=True)

    class Meta:
        fields = ["email", "role"]

    def validate(self, attrs):
        project = self.context.get("project_id", None)
        if project is None:
            raise serializers.ValidationError({"project_id": "project id is valid"})

        email = attrs.get("email", None)
        if email is None:
            raise serializers.ValidationError({"email": "email is valid"})

        if ProjectInvitation.objects.filter(project=project, email=email).exists():
            raise serializers.ValidationError(
                {"invite": "This user has already exists in database"}
            )

        return attrs
