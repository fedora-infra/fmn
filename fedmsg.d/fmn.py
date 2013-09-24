import socket
hostname = socket.gethostname().split('.')[-1]

config = {
    "fmn.consumer.enabled": True,
    "fmn.sqlalchemy.uri": "sqlite:////var/tmp/fmn-dev-db.sqlite",
    "endpoints": {
        "fmn.%s" % hostname: [
            "tcp://127.0.0.1:3041",
        ],
    },
    "logging": dict(
        loggers=dict(
            fmn={
                "level": "DEBUG",
                "propagate": False,
                "handlers": ["console"],
            },
        ),
    ),
}
