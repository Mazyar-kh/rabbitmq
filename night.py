import pika
import ssl

ssl_options = {
    "ssl_version": ssl.PROTOCOL_TLSv1_2,
    "ca_certs": "/path/to/ca_certificate.pem",
    "certfile": "/path/to/client_certificate.pem",
    "keyfile": "/path/to/client_key.pem",
    "cert_reqs": ssl.CERT_REQUIRED
}

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='your_host',
        port=5671,
        virtual_host='your_vhost',
        credentials=pika.credentials.PlainCredentials(
            username='your_username',
            password='your_password'
        ),
        ssl=True,
        ssl_options=ssl_options
    )
)

channel = connection.channel()
