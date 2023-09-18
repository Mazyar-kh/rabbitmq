import pika
import ssl

context = ssl.create_default_context(cafile='/etc/rabbitmq/tls-gen/basic/result/ca_certificate.pem')
context.load_cert_chain(certfile='/etc/rabbitmq/tls-gen/basic/result/client_maz-virtual-machine_certificate.pem', keyfile='/etc/rabbitmq/tls-gen/basic/result/client_maz-virtual-machine_key.pem', password="bunnies")
ssl_options = pika.SSLOptions(context)

parameters = pika.ConnectionParameters(
    host='localhost',
    port=5671,
    virtual_host='/',
    credentials=pika.PlainCredentials('guest', 'guest'),
    ssl_options=ssl_options
)

def callback(ch, method, properties, body):
    print("Received message:", body.decode())

try:
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    
    queue_name = "my_queue"
    channel.queue_declare(queue=queue_name)
    channel.exchange_declare(exchange='my_exchange', exchange_type='direct')
    
    channel.queue_bind(exchange='my_exchange', queue=queue_name, routing_key='my_queue')
    
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    
    print("Waiting for messages...")

    channel.start_consuming()

except pika.exceptions.AMQPConnectionError as e:
    print("An error occurred while connecting to RabbitMQ:", str(e))
