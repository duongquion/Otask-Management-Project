from django.urls import path

from .views.api import UserAPIView, UserDetailAPIView

user_api_urls = [
    path("list/", UserAPIView.as_view(), name="api-list-user"),
    path("profile/", UserDetailAPIView.as_view(), name="api-detail-user"),
]
