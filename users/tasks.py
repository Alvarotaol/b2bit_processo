# users/tasks.py
from celery import shared_task
from django.core.mail import send_mail, BadHeaderError
import logging

logger = logging.getLogger(__name__)
@shared_task
def send_new_follower_email(followed_user_email, follower_username):
    try:
        subject = "Novo seguidor no MiniTwitter!"
        message = f"Você acabou de ganhar um novo seguidor: {follower_username}!"
        from_email = "no-reply@minitwitter.com"
        recipient_list = [followed_user_email]

        send_mail(subject, message, from_email, recipient_list)
        logger.info(f"E-mail enviado para {followed_user_email}")
    except BadHeaderError:
        logger.error("Invalid header found when trying to send email.")
    except Exception as e:
        logger.error(f"Erro ao enviar email: {str(e)}")