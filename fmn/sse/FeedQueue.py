import pika


class FeedQueue:
    def __init__(self, host='localhost',
                 exchange='',
                 queue_name='skrzepto.id.fedoraproject.org',
                 expire_ms=1*60*60*1000,
                 port=5672):

        self.host = host
        self.exchange = exchange
        self.queue_name = queue_name
        self.expire_ms = expire_ms
        self.port = port

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
            return ''

        if method_frame.NAME == 'Basic.GetEmpty':
            return ''
        else:
            self.channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            return body.decode('utf-8')

    def push_message(self, msg):
        self._check_connection()

        if self.channel.basic_publish(exchange=self.exchange,
                                      routing_key=self.exchange + '-' + self.queue_name,
                                      body=msg,
                                      properties=pika.BasicProperties(
                                          delivery_mode=2)):
            print('message sent')
        else:
            print('ERROR: message failed to send')

    def _get_pika_channel_connection(self):
        """ Connect to pika server and return channel and connection"""
        parameters = pika.ConnectionParameters(host=self.host, port=self.port)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.exchange_declare(exchange=self.exchange)
        channel.queue_declare(queue=self.queue_name, durable=True,
                              arguments={'x-message-ttl': self.expire_ms, })
        channel.queue_bind(queue=self.queue_name,
                           exchange=self.exchange,
                           routing_key=self.exchange + '-' + self.queue_name)
        return channel, connection
