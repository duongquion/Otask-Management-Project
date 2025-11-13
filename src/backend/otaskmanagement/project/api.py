from rest_framework.response import Response
from rest_framework import permissions, status

from otaskmanagement.mixins import OtaskMixinDetailView

from .serializers import WriteProjectMembershipSerializer, ProjectMembershipSerializer
from .models import Project, ProjectMembership

METHOD = ["POST", "PUT", "PATCH", "DELETE"]

class ProjectMembershipView(OtaskMixinDetailView):
    
    permission_classes = [permissions.IsAuthenticated]
    queryset = ProjectMembership.objects.select_related("member","project")
    lookup_field = "pk"
    lookup_url_kwarg ="pk"
    
    def get_serializer_class(self):
        if self.request.method in METHOD:
            return WriteProjectMembershipSerializer
        return ProjectMembershipSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = {
            "MESSAGE": "SUCCESSFULLY",
            "DATA": response.data
        }
        return response


    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        response.data = {
            "MESSAGE": "SUCCESSFULLY",
            "DATA": response.data
        }
        return response
