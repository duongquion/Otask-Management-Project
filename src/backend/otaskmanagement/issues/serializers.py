from rest_framework import serializers

from .models import Sprint


class SprintSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Sprint
        fields = ["id", "name", "start_date", "end_date", "is_closed", "project"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        view = self.context["view"]
        project_id = view.kwargs.get("project_id")

        if Sprint.objects.filter(name=attrs["name"], project_id=project_id).exists():
            raise serializers.ValidationError(
                {"name": "Sprint name already exists in this project."}
            )

        start_date = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end_date = attrs.get("end_date", getattr(self.instance, "end_date", None))

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError(
                {"end_date": "End date must be after start date."}
            )

        return attrs
