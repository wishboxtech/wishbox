from asgiref.sync import async_to_sync

from settings import SMS_STREAM, SMS_SUBJECT
from src.utils.nats.publish import publish


@async_to_sync
async def send_sms_otp(phone, otp):
    await publish(
        data={"phone": phone, "code": otp},
        subject=SMS_SUBJECT,
        stream=SMS_STREAM,
    )
