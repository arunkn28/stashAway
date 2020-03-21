import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()

channel.queue_declare(queue='workflow')


def callback(ch, method, properties, body):
    print("Workflow received" % body)


channel.basic_consume(
    queue='workflow', on_message_callback=callback, auto_ack=True)

channel.start_consuming()