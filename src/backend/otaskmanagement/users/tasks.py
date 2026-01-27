from datetime import datetime

from celery import shared_task

# from users.models import CustomUser

# @shared_task
# def get_user(user_email):
#     users = list(CustomUser.objects.filter(email=user_email).values('id', 'email'))
#     print(f"======[RESULT: {users}]======", )


@shared_task
def test_print_task():
    now = datetime.now().strftime("%H:%M:%S")
    message = f"✅ [TEST] Celery đang chạy tốt! Giờ hiện tại: {now}"

    # Lệnh print này sẽ hiện ra trong log của container
    print(message)

    return "Done"
