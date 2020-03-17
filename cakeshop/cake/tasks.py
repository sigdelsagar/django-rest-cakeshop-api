from __future__ import absolute_import, unicode_literals
from celery import shared_task
from cakeshop.celery import app
from kombu import Connection, Exchange, Queue


import time


@app.task
def add(x, y):
    time.sleep(5)
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)


@shared_task
def publish_message(message):
    # task_queue = Queue('tasks', Exchange('tasks'), routing_key='tasks')
    with app.producer_pool.acquire(block=True) as producer:
        producer.publish(
            {'message': message},
            serializer='json',
            # exchane=task_queue.exchange,
            # exchange='myexchange',
            # routing_key='mykey',
            exchange='celery',
            routing_key='celery',
            # headers={
            #     'lang':  'py',
            #     'task': 'string task',
            #     'id': 'uuid task_id'
            # }
        )
