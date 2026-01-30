"""Provides JSON API endpoints for the Project app."""

from otaskmanagement.mixins import ListAPI, OtaskMixinDetailView
from otaskmanagement.permissions import CheckAPIPermission
from otaskmanagement.utils import METHOD
from rest_framework import permissions

from .models import Project, ProjectMembership
from .serializers import (
    ProjectMembershipSerializer,
    ProjectSerializer,
    WriteProjectMembershipSerializer,
)


class ProjectAPIView(ListAPI):
    """Returns a read-only list of Project records."""

    permission_classes = [permissions.IsAuthenticated, CheckAPIPermission]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    required_permission = "view_project"


class ProjectMembershipAPIView(OtaskMixinDetailView):
    """Handles CRUD operations for ProjectMembership."""

    permission_classes = [permissions.IsAuthenticated, CheckAPIPermission]
    queryset = ProjectMembership.objects.select_related("member", "project")
    required_permission = "view_project"

    def get_project(self):
        return self.kwargs.get("pk")

    def get_serializer_class(self):
        if self.request.method in METHOD:
            return WriteProjectMembershipSerializer
        return ProjectMembershipSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {"MESSAGE": "SUCCESSFULLY", "DATA": response.data}
        return response

    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        response.data = {"MESSAGE": "SUCCESSFULLY", "DATA": response.data}
        return response
