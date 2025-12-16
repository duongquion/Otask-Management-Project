from django.urls import include, path
from issues.api import SprintDetail, SprintList

sprint_api_urls = [
    path(
        "<uuid:project_id>/",
        include(
            [
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
        ),
    ),
]
