from rest_framework import serializers
from users.ruleset import RoleEnum


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    role = serializers.ChoiceField(choices=RoleEnum.choices, required=True)

    class Meta:
        fields = ["email", "role"]
