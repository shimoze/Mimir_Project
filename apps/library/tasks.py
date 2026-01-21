from celery import shared_task
import time

@shared_task
def send_welcome_email(username):
    time.sleep(5)
    print(f"📧 Письмо для {username} успешно отправлено!")
    return "Done"