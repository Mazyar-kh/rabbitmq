from kombu import Connection, Exchange, Queue, Producer

# Define your connection parameters
hostname = 'your_hostname'
port = 'your_port'
userid = 'your_userid'
password = 'your_password'
virtual_host = 'your_virtual_host'

# Create a connection
conn = Connection(
    hostname=hostname,
    port=port,
    userid=userid,
    password=password,
    virtual_host=virtual_host,
    heartbeat=10  # Set the heartbeat parameter
)

# Create an exchange
exchange = Exchange('my_exchange', type='direct')

# Create a queue
queue = Queue('my_queue', exchange=exchange, routing_key='my_routing_key')

# Bind the queue to the exchange
queue.queue_bind()

# Create a producer
with conn.Producer() as producer:
    # Publish messages to the exchange
    producer.publish('Hello, World!', routing_key='my_routing_key')
