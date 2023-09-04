import pika, sys, os, ssl

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



def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
    channel = connection.channel()

    queue_name = "my_queue"
    channel.queue_declare(queue=queue_name)
    channel.exchange_declare(exchange='my_exchange', exchange_type='direct')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue='my_queue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
