"""Provides URLs for the Project app."""

from django.urls import path

from .api import ProjectAPIView, ProjectMembershipAPIView

urlpatterns = [
    path("", ProjectAPIView.as_view(), name="project-list"),
    path(
        "managed/",
        ProjectMembershipAPIView.as_view(),
        name="project-membership-list-create",
    ),
    path(
        "managed/<uuid:pk>/",
        ProjectMembershipAPIView.as_view(),
        name="project-membership-detail",
    ),
]
