import json


class Handler:
    def __init__(self, config):
        self._config = config

    def setup(self):
        # Here we connect to the destination server if relevant.
        pass

    def stop(self):
        pass

    def on_message(self, channel, method_frame, header_frame, body):
        try:
            self.handle(json.loads(body))
        except Exception:
            channel.basic_nack(delivery_tag=method_frame.delivery_tag)
            raise
        else:
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def handle(self, message):
        raise NotImplementedError


class PrintHandler(Handler):
    def handle(self, message):
        print("Received:", message)
