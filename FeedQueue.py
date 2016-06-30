import pika


class FeedQueue:
    def __init__(self, host='localhost',
                 queue_name='skrzepto.id.fedoraproject.org',
                 expire_ms=1*60*60*1000):

        self.host = host
        self.queue_name = queue_name
        self.expire_ms = expire_ms

        self.channel, self.connection = self._get_pika_channel_connection()

    def _check_connection(self):
        if self.connection.is_closed:
            self.channel, self.connection = self._get_pika_channel_connection()

    def receive_one_message(self):
        # modified but src is below
        # src: http://stackoverflow.com/questions/9876227/rabbitmq-consume-one-message-if-exists-and-quit

        self._check_connection()

        method_frame, header_frame, body = self.channel.basic_get(
            queue=self.queue_name)
        if not method_frame:
            self.connection.close()
            return ''

        if method_frame.NAME == 'Basic.GetEmpty':
            self.connection.close()
            return ''
        else:
            self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            self.connection.close()
            # print body
            return body

    def push_message(self, msg):
        self._check_connection()

        if self.channel.basic_publish(exchange='',
                                      routing_key=self.queue_name,
                                      body=msg,
                                      properties=pika.BasicProperties(
                                          delivery_mode=2)):
            print('message sent')
        else:
            print('ERROR: message failed to send')

    def _get_pika_channel_connection(self):
        """ Connect to pika server and return channel and connection"""
        parameters = pika.ConnectionParameters(host=self.host)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name, durable=True,
                              arguments={'x-message-ttl': self.expire_ms, })
        return channel, connection
