import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Celery

from src.core.settings import settings

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_REDIS_URL
celery.conf.result_backend = settings.CELERY_REDIS_URL


@celery.task(name="send_email_task")
def send_email_task(subject, text, to) -> None:
    message: MIMEMultipart = _build_message(subject, text, to)
    _send_email(message)


def _build_message(subject: str, text: str, to: str) -> MIMEMultipart:
    message = MIMEMultipart()
    message["From"] = settings.SMTP_EMAIL
    message["To"] = to
    message["Subject"] = subject
    message.attach(MIMEText(text, "plain"))
    return message


def _send_email(message):
    context: smtplib.SSLContext = ssl.create_default_context()
    server = smtplib.SMTP_SSL(
        settings.SMTP_HOST,
        settings.SMTP_PORT,
        context=context,
    )
    server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
    server.send_message(message)
    server.quit()
