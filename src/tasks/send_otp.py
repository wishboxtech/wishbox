from celery import shared_task
from src.core.rabbitmq import rabbitmq
import json


@shared_task
def send_otp(data):
    rabbitmq.publish_message(data, routing_key="otp")
    print(f"otp message sent: {data}")