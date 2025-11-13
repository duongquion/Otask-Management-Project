"""Provides JSON API endpoints for the Project app."""

from rest_framework import permissions

from otaskmanagement.mixins import OtaskMixinDetailView, ListAPIView

from .serializers import (
    WriteProjectMembershipSerializer,
    ProjectMembershipSerializer,
    ProjectSerializer,
)
from .models import Project, ProjectMembership

METHOD = ["POST", "PUT", "PATCH", "DELETE"]


class ProjectAPIView(ListAPIView):
    """Returns a read-only list of Project records."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectMembershipAPIView(OtaskMixinDetailView):
    """Handles CRUD operations for ProjectMembership."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = ProjectMembership.objects.select_related("member", "project")
    lookup_field = "pk"
    lookup_url_kwarg = "pk"

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
