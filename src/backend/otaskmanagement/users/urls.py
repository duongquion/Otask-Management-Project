from django.urls import path

from .api import UserAPIView

urlpatterns = [path("", UserAPIView.as_view(), name="user-api")]
