from __future__ import absolute_import, unicode_literals

import os
from kombu import Connection, Exchange, Queue, Consumer
from celery import Celery, bootsteps

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cakeshop.settings')

app = Celery(
    'cakeshop', broker='amqp://nqlsogcb:SihkJMSxzFBBXfsiSJ9Q2ToSCBWGNX63@rhino.rmq.cloudamqp.com/nqlsogcb',)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
# task_queue = Queue('tasks', Exchange('tasks'), routing_key='tasks')
# CELERY_QUEUES
with app.pool.acquire(block=True) as conn:
    exchange = Exchange(
        name='myexchange',
        type='direct',
        durable=True,
        channel=conn,
    )
    exchange.declare()
    queue = Queue(
        name='myqueue',
        exchange=exchange,
        routing_key='mykey',
        channel=conn,
        # x-message_ttl=600,
        queue_arguments={
            'x-queue-type': 'classic'
        },
        durable=True
    )
    queue.declare()


class InputMessageConsumerStep(bootsteps.ConsumerStep):
    def get_consumers(self, channel):
        return [Consumer(channel,
                         queues=[queue],
                         callbacks=[self.handle_message],
                         accept=["json"])]

    def handle_message(self, body, message):
        print('Received message:{0!r}'.format(body))
        message.ack()


app.steps["consumer"].add(InputMessageConsumerStep)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# if __name__ == "__main__":
#     app.start()
