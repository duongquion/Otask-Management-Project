from django.shortcuts import get_object_or_404
from issues.models import Sprint
from issues.serializers import (
    SprintSerializer,
)
from project.models import Project
from rest_framework import permissions
from rest_framework.exceptions import ValidationError

from otaskmanagement.mixins import (
    ListCreateAPI,
    RetrieveUpdateDestroyAPI,
)


class SprintMixin:
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SprintSerializer


class SprintList(SprintMixin, ListCreateAPI):

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        if not project_id:
            raise ValidationError({"project_id": "This field is required."})
        return Sprint.objects.filter(project_id=project_id)

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        serializer.save(project=project)


class SprintDetail(SprintMixin, RetrieveUpdateDestroyAPI):

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        if not project_id:
            raise ValidationError({"project_id": "This field is required."})
        return Sprint.objects.filter(project_id=project_id)
