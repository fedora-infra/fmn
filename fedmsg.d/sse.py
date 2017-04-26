config = {

    # SSE
    "fmn.sse.pika.host": "localhost",
    "fmn.sse.pika.port": 5672,
    "fmn.sse.pika.msg_expiration": 3600000,  # 1 hour in ms

    # SSE Web server configuration
    "fmn.sse.webserver.tcp_port": 8080,
    # A list of interfaces to listen to ('127.0.0.1', for example); if none
    # are specified the server listens on all available interfaces.
    'fmn.sse.webserver.interfaces': [],

    # A regular expression using the standard Python re syntax that defines a
    # whitelist of queues exposed by the SSE server.
    'fmn.sse.webserver.queue_whitelist': '.+\.id\.fedoraproject\.org$',

    # A regular expression using the standard Python re syntax that defines a
    # blacklist for queues exposed by the SSE server. Any queue name that is
    # matched by the regular expression will return a HTTP 403 to the client.
    #
    # Note: This is applied _after_ the whitelist so if the queue is matched
    # by both regular expressions, the queue _will not_ be served.
    'fmn.sse.webserver.queue_blacklist': None,

    # The value to use with the 'Access-Control-Allow-Origin' HTTP header
    'fmn.sse.webserver.allow_origin': '*',

    # Define how many messages to prefetch from the AMQP server
    'fmn.sse.pika.prefetch_count': 5,

    'endpoints': {
        # Just need this entry here for tests to pass on travis-ci.
    }
}
