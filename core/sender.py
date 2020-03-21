import pika


class RabbitMQPusher(object):
    def __init__(self):
        try:
            self.connection = self.create_connection()
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='workflow')
        except Exception as e:
            print("Error while connecting to rmq server")

    def create_connection(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='127.0.0.1'))
        return connection

    def push_to_queue(self, data):
        try:
            self.channel.basic_publish(exchange='', routing_key='workflow', body=data)
        except Exception as e:
            print("Could not push to queue")

    def __del__(self):
        self.connection.close()
