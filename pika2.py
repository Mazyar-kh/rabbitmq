import functools
import logging
import pika
import threading
import time
import ssl
import socket

LOG_FORMAT = (
    '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
    '-35s %(lineno) -5d: %(message)s'
)
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)


def ack_message(channel, delivery_tag):
    """
    Note that `channel` must be the same pika channel instance via which
    the message being ACKed was retrieved (AMQP protocol constraint).
    """
    if channel.is_open:
        channel.basic_ack(delivery_tag)
    else:
        # Channel is already closed, so we can't ACK this message;
        # log and/or do something that makes sense for your app in this case.
        pass


def do_work(connection, channel, delivery_tag, body):
    thread_id = threading.get_ident()
    fmt1 = 'Thread id: {} Delivery tag: {} Message body: {}'
    LOGGER.info(fmt1.format(thread_id, delivery_tag, body))

    # Sleeping to simulate 10 seconds of work
    time.sleep(10)

    cb = functools.partial(ack_message, channel, delivery_tag)
    connection.add_callback_threadsafe(cb)


def on_message(channel, method_frame, header_frame, body, args):
    (connection, threads) = args
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=do_work, args=(connection, channel, delivery_tag, body))
    t.start()
    threads.append(t)


credentials = pika.PlainCredentials('guest', 'guest')

# Enable TLS connection
ssl_context = ssl.create_default_context(cafile="/home/kk/testca/cacert.pem")
ssl_context.check_hostname = False
ssl_context.load_cert_chain(certfile="/home/kk/client/cert.pem", keyfile="/home/kk/client/key.pem")

parameters = pika.ConnectionParameters(
    host='127.0.0.1',
    port=5671,
    credentials=credentials,
    ssl=True,
    ssl_options=ssl_context.wrap_socket(socket.socket())
)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange="test_exchange", exchange_type="direct", passive=False, durable=True, auto_delete=False)
channel.queue_declare(queue="standard", auto_delete=True)
channel.queue_bind(queue="standard", exchange="test_exchange", routing_key="standard_key")
channel.basic_qos(prefetch_count=1)

threads = []
on_message_callback = functools.partial(on_message, args=(connection, threads))
channel.basic_consume(on_message_callback, 'standard')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

# Wait for all to complete
for thread in threads:
    thread.join()

connection.close()

======================================================
import functools
import logging
import pika
import threading
import time
import ssl

LOG_FORMAT = (
    '%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
    '-35s %(lineno) -5d: %(message)s'
)
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

def ack_message(channel, delivery_tag):
    """
    Note that `channel` must be the same pika channel instance via which
    the message being ACKed was retrieved (AMQP protocol constraint).
    """
    if channel.is_open:
        channel.basic_ack(delivery_tag)
    else:
        # Channel is already closed, so we can't ACK this message;
        # log and/or do something that makes sense for your app in this case.
        pass

def do_work(connection, channel, delivery_tag, body):
    thread_id = threading.get_ident()
    fmt1 = 'Thread id: {} Delivery tag: {} Message body: {}'
    LOGGER.info(fmt1.format(thread_id, delivery_tag, body))

    # Sleeping to simulate 10 seconds of work
    time.sleep(10)

    cb = functools.partial(ack_message, channel, delivery_tag)
    connection.add_callback_threadsafe(cb)

def on_message(channel, method_frame, header_frame, body, args):
    (connection, threads) = args
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=do_work, args=(connection, channel, delivery_tag, body))
    t.start()
    threads.append(t)

credentials = pika.PlainCredentials('guest', 'guest')

# Enable TLS connection
ssl_context = ssl.create_default_context(cafile="/home/kk/testca/cacert.pem")
ssl_context.check_hostname = False
ssl_context.load_cert_chain(certfile="/home/kk/client/cert.pem", keyfile="/home/kk/client/key.pem")

parameters = pika.ConnectionParameters(
    host='127.0.0.1',
    port=5671,
    credentials=credentials,
    ssl=True,
)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange="test_exchange", exchange_type="direct", passive=False, durable=True, auto_delete=False)
channel.queue_declare(queue="standard", auto_delete=True)
channel.queue_bind(queue="standard", exchange="test_exchange", routing_key="standard_key")
channel.basic_qos(prefetch_count=1)

threads = []
on_message_callback = functools.partial(on_message, args=(connection, threads))
channel.basic_consume(on_message_callback, 'standard')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

# Wait for all to complete
for thread in threads:
    thread.join()

connection.close()
======================================================








  ssl_options=ssl_context.wrap_socket(socket.socket())
NameError: name 'socket' is not defined




 raise TypeError(
TypeError: ssl_options must be None or SSLOptions but got <ssl.SSLSocket fd=3, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 0)>


