from django.urls import path
from common.api import TestEmail

urlpatterns = [
    path("test/", TestEmail.as_view(), name="test-email"),
]
