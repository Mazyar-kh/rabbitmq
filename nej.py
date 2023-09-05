
import ssl
import pika
# Configure SSL/TLS options
ssl_options = {
   "cert_reqs": ssl.CERT_REQUIRED,
    "ca_certs": "/root/tls-gen/basic/result/ca_certificate.pem",
    "keyfile": "/root/tls-gen/basic/result/client_maz-virtual-machine_key.pem",
    "certfile": "/root/tls-gen/basic/result/client_maz-virtual-machine_certificate.pem",
}

# Create a connection to RabbitMQ server
parameters = pika.ConnectionParameters(
    host="127.0.0.1",
    port=5671,  # Use the default RabbitMQ SSL port
    virtual_host="/",
    credentials=pika.credentials.PlainCredentials("guest", "guest"),
#    ssl = True,
    ssl_options=None,
)

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

# Declare a queue
queue_name = "my_queue"
channel.queue_declare(queue=queue_name)
channel.exchange_declare(exchange='my_exchange', exchange_type='direct')

# Publish a message
message = "Hello, RabbitMQ!"
channel.basic_publish(exchange="my_exchange", routing_key=queue_name, body=message)

print(f"Message sent: {message}")

# Close the connection
connection.close()
