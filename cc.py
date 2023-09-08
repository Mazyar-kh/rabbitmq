import pika
import ssl

context = ssl.create_default_context(cafile='/root/example.com.crt')
context.load_cert_chain(certfile='/root/example.com.crt', keyfile='/root/example.com.key.org', password="mazyar")
ssl_options = pika.SSLOptions(context)

parameters = pika.ConnectionParameters(
host='127.0.0.1',
port=5671,
virtual_host='/',
credentials=pika.PlainCredentials('guest', 'guest'),
ssl_options=ssl_options
)


try:
    # Connect to RabbitMQ server
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declare a queue
    queue_name = "my_queue"
    channel.queue_declare(queue=queue_name)
    channel.exchange_declare(exchange='my_exchange', exchange_type='direct')

    # Bind the queue to the exchange
    channel.queue_bind(exchange='my_exchange', queue=queue_name, routing_key='my_queue')

    # Publish a message
    message = "Hello, RabbitMQ!"
    channel.basic_publish(exchange='my_exchange', routing_key='my_queue', body=message)
    print(f"Message sent: {message}")

    # Close the connection
    connection.close()

except pika.exceptions.AMQPConnectionError as e:
    print("An error occurred while connecting to RabbitMQ:", str(e))
