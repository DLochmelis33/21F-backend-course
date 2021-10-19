import pika


def do_logging():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='log')

    def callback(ch, method, properties, body):
        print(f'Logging: \'{body}\'')

    channel.basic_consume(queue='log', on_message_callback=callback, auto_ack=True)

    print('to stop press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    do_logging()
