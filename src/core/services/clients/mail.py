from dataclasses import dataclass

from src.worker.celery import send_email_task


@dataclass
class MailClient:
    def send_welcome_email(self, to: str) -> None:
        subject = "Welcome email"
        body = "Welcome to pomodoro"
        return send_email_task.delay(subject, body, to)
