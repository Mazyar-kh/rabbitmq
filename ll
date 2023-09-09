[
  {rabbit, [
     {ssl_listeners, [5671]},
     {tcp_listeners, []},
     {ssl_options, [{cacertfile, "/home/vv/tls-gen/basic/result/ca_certificate.pem"},
                    {certfile,   "/home/vv/tls-gen/basic/result/client_vv-virtual-machine_certificate.pem"},
                    {keyfile,    "/home/vv/tls-gen/basic/result/client_vv-virtual-machine_key.pem"},
                    {verify,     verify_peer},
                    {fail_if_no_peer_cert, true}]}
   ]}
].


import pika
import ssl

# RabbitMQ connection parameters
credentials = pika.PlainCredentials('guest', 'guest')
ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations('/home/vv/tls-gen/basic/result/ca_certificate.pem')
ssl_context.load_cert_chain(
    certfile='/home/vv/tls-gen/basic/result/client_vv-virtual-machine_certificate.pem',
    keyfile='/home/vv/tls-gen/basic/result/client_vv-virtual-machine_key.pem'
)

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





  File "/home/vv/Downloads/client2*.py", line 22, in <module>
    connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
  File "/usr/local/lib/python3.10/dist-packages/pika/adapters/blocking_connection.py", line 360, in __init__
    self._impl = self._create_connection(parameters, _impl_class)
  File "/usr/local/lib/python3.10/dist-packages/pika/adapters/blocking_connection.py", line 451, in _create_connection
    raise self._reap_last_connection_workflow_error(error)
pika.exceptions.AMQPConnectionError











