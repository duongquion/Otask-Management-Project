from django.urls import path
from .api import ProjectMembershipView

urlpatterns = [
    path("", ProjectMembershipView.as_view(), name="project-view"),
    path("<uuid:pk>/", ProjectMembershipView.as_view(), name="project-view"),
]