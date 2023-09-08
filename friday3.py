import pika
import ssl

# RabbitMQ connection parameters
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile='/etc/rabbitmq/client/cert.pem', keyfile='/etc/rabbitmq/client/key.pem')
ssl_context.load_verify_locations(cafile='/etc/rabbitmq/testca/cacert.pem')
ssl_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
ssl_context.options |= ssl.OP_SINGLE_DH_USE
ssl_context.set_ciphers('HIGH:!DH:!aNULL')
cert_reqs=ssl.CERT_REQUIRED

credentials = pika.credentials.ExternalCredentials()

parameters = pika.ConnectionParameters(
    host='127.0.0.1',
    port=5671,
    virtual_host='/',
    credentials=credentials,
    ssl_options=pika.SSLOptions(ssl_context)
)

# Connect to RabbitMQ server
connection = pika.BlockingConnection(parameters)
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
