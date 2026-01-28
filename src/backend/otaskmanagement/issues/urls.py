from django.urls import path

from issues.api import SprintDetail, SprintList

sprint_api_urls = [
    path(
        "",
        SprintList.as_view(),
        name="api-sprint-list-create",
    ),
    path(
        "<uuid:pk>/",
        SprintDetail.as_view(),
        name="api-sprint-detail",
    ),
]
