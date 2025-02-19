import json
import uuid
from dataclasses import dataclass

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractRobustConnection

from src.core.settings import settings


@dataclass
class MailClient:
    async def send_welcome_email(self, to: str) -> None:
        email_content: dict[str, str] = {
            "subject": "Welcome email",
            "body": "Welcome to pomodoro",
            "email": to,
        }
        connection: AbstractRobustConnection = await aio_pika.connect_robust(
            settings.AMQP_BROKER_URL,
        )
        async with connection:
            channel: AbstractChannel = await connection.channel()
            message = aio_pika.Message(
                body=json.dumps(email_content).encode("utf-8"),
                correlation_id=str(uuid.uuid4()),
                reply_to="callback_mail_queue",
            )
            await channel.default_exchange.publish(
                message=message,
                routing_key="email_queue",
            )
