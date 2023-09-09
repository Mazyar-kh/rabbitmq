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

# Create a producer
with conn.Producer() as producer:
    # Your message publishing code here
