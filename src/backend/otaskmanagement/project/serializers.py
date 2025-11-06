from rest_framework import serializers
from .models import Project, ProjectMembership


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project