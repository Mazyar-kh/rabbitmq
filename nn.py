import pika
import ssl

# SSL context-test
#ssl._create_default_https_context = ssl._create_unverified_context
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile='/root/tls-gen/basic/result/client_maz-virtual-machine_certificate.pem', keyfile='/root/tls-gen/basic/result/client_maz-virtual-machine_key.pem')

# RabbitMQ connection parameters
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters(host='127.0.0.1',
                                       port=5671,
                                       virtual_host='/',
                                       credentials=credentials,
                                       ssl_options=pika.SSLOptions(ssl_context))

# Connect to RabbitMQ server
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare a queue and exchange
channel.queue_declare(queue='my_queue')
channel.exchange_declare(exchange='my_exchange', exchange_type='direct')

# Publish a message to the queue
channel.basic_publish(exchange='my_exchange',
                      routing_key='',
                      body='Hello, RabbitMQ!')

# Close the connection
connection.close()
