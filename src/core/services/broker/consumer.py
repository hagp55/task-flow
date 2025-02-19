import json
import logging

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractQueue, AbstractRobustConnection

from src.core.settings import settings

logger = logging.getLogger(__name__)


async def get_broker_connection() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(
        settings.AMQP_BROKER_URL,
    )


async def consume_email_fail(message: aio_pika.IncomingMessage) -> None:
    async with message.process():
        mail = json.loads(message.body.decode())
        correlation_id = message.correlation_id
        logger.error(f"{mail}, {correlation_id=}")


async def make_amqp_consumer() -> None:
    connection: AbstractRobustConnection = await get_broker_connection()
    channel: AbstractChannel = await connection.channel()
    queue: AbstractQueue = await channel.declare_queue(
        "callback_mail_queue",
        durable=True,
    )
    await queue.consume(consume_email_fail)  # type: ignore
