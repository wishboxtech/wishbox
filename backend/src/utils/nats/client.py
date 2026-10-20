from nats.aio.client import Client as NATS

from settings import NATS_URL


class NCSC:
    js = None
    nc = None
    is_connected = False

    def __init__(self):
        self.nc = NATS()
        self.js = self.nc.jetstream()
        # IMPORTANT NOTE
        # You have to create the stream at least once
        # js.add_stream(name="sms-stream", subjects=["sms.otp"])

    async def connect(self):
        if self.is_connected:
            return

        await self.nc.connect(NATS_URL)

        self.is_connected = True

    async def disconnect(self):
        await self.nc.close()
