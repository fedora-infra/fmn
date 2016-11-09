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

    'endpoints': {
        # Just need this entry here for tests to pass on travis-ci.
    }
}
