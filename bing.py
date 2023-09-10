import pika

ssl_options = pika.SSLOptions(
    ssl_version=ssl.PROTOCOL_TLSv1_2,
    ca_certs="/path/to/ca_certificate.pem",
    keyfile="/path/to/client_key.pem",
    certfile="/path/to/client_certificate.pem",
    cert_reqs=ssl.CERT_REQUIRED
)

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters(
    host='localhost',
    port=5671,
    virtual_host='/',
    credentials=credentials,
    ssl_options=ssl_options
)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()
