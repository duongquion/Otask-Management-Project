from django.urls import path
from common.api import AcceptInvitation, SendEmailMember, VerifyInvitation

urlpatterns = [
    path(
        "send-mail/<uuid:pk>/",
        SendEmailMember.as_view(),
        name="api-send-mail",
    ),
    path(
        "invite/verify/",
        VerifyInvitation.as_view(),
        name="api-verified-invite",
    ),
    path(
        "invite/accept/",
        AcceptInvitation.as_view(),
        name="api-accepted-invite",
    ),
]
