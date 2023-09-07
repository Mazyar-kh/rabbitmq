import pika
import ssl

# RabbitMQ connection parameters
credentials = pika.PlainCredentials('guest', 'guest')
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(
       ca_certs='/home/vv/testca/cacert.pem',
        keyfile='/home/vv/client/key.pem',
        certfile='/home/vv/client/cert.pem',
        cert_reqs=ssl.CERT_REQUIRED
)
#connection = pika.BlockingConnection(parameters)
parameters = pika.ConnectionParameters(
    host='127.0.0.1',
    port=5671,
    virtual_host='/',
    credentials=credentials,
    ssl_options=pika.SSLOptions(ssl_context)
)

# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

# Declare a queue and an exchange
queue_name = "my_queue"
exchange_name = "my_exchange"

channel.queue_declare(queue=queue_name, durable=True)
channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

# Bind the queue to the exchange
channel.queue_bind(queue=queue_name, exchange=exchange_name)

# Publish a persistent message to the exchange
message = "Hello, RabbitMQ!"
channel.basic_publish(
    exchange=exchange_name,
    routing_key=queue_name,
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2  # make message persistent
    )
)
print(f"Message sent: {message}")

# Close the connection
connection.close()
