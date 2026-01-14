import logging
from celery import shared_task
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task
def send_project_invite_email(to_email, verify_url, project_name):
    subject = f"You've been invited to join project {project_name}"
    text_content = (
        f"You have been invited to join project {project_name}.\n"
        f"Open this link to accept:\n{verify_url}"
    )
    from django.template.loader import render_to_string

    html_content = render_to_string(
        "email/project_invite.html",
        {
            "project_name": project_name,
            "verify_url": verify_url,
        },
    )

    try:
        from django.core.mail import EmailMultiAlternatives

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        email.attach_alternative(html_content, "text/html")
        result = email.send(fail_silently=False)

        if result == 0:
            logger.warning("No emails were sent.")

        logger.info("Successfully for send the email")

    except Exception as e:
        logger.warning(f"[ERROR]: {e}")
