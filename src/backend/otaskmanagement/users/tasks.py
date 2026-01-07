from celery import shared_task

from users.models import CustomUser

@shared_task
def get_user(user_email):
    users = list(CustomUser.objects.filter(email=user_email).values('id', 'email'))
    print(f"======[RESULT: {users}]======", )