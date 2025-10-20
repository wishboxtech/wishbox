import pika
import json
from django.conf import settings

class RabbitMQPublisher:
    def __init__(self):
        self.connection = None
        self.channel = None
        self._connect()

    def _connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=settings.RABBITMQ_HOST,
                    port=settings.RABBITMQ_PORT,
                    virtual_host=settings.RABBITMQ_VHOST,
                    credentials=pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
                )
            )
            self.channel = self.connection.channel()
            print("Connected to RabbitMQ")
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Error connecting to RabbitMQ: {e}")
            self.connection = None
            self.channel = None

    def publish_message(self,  message, exchange_name: str = "", routing_key: str = ""):
        if not self.channel:
            self._connect()
            if not self.channel:
                print("Failed to establish RabbitMQ connection, cannot publish message.")
                return

        try:
            # self.channel.exchange_declare(exchange=exchange_name, exchange_type='topic', durable=True)
            self.channel.basic_publish(
                exchange=exchange_name,
                routing_key=routing_key,
                body=json.dumps(message).encode('utf-8'),
            )
            print(f"Message published to exchange '{exchange_name}' with routing key '{routing_key}'")
        except pika.exceptions.AMQPChannelError as e:
            print(f"Error publishing message: {e}")
            self._connect() # Attempt to reconnect on channel error
        except Exception as e:
            print(f"An unexpected error occurred while publishing: {e}")

    def close_connection(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
            print("RabbitMQ connection closed.")

rabbitmq = RabbitMQPublisher()