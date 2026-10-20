import json

from src.utils.nats.client import NCSC


async def publish(data: dict, subject: str, stream: str = None):
    NATS_OBJECT = NCSC()
    await NATS_OBJECT.connect()
    await NATS_OBJECT.js.publish(
        subject,
        bytes(json.dumps(data, ensure_ascii=False), encoding="UTF-8"),
    )
    await NATS_OBJECT.disconnect()
