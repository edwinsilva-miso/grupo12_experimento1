import os
import json
import pika


RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
PRODUCTS_ROUTING_KEY = os.getenv('PRODUCTS_ROUTING_KEY')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    )
)
channel = connection.channel()
channel.queue_declare(queue=PRODUCTS_ROUTING_KEY, durable=True)


def callback(ch, method, properties, body):
    print(f'<< Received: {body}')
    ch.basic_ack(delivery_tag=method.delivery_tag)
    # process the message
    # for example, save them to database

channel.basic_consume(queue=PRODUCTS_ROUTING_KEY, on_message_callback=callback)
channel.start_consuming()




