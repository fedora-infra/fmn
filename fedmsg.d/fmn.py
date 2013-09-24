import socket
hostname = socket.gethostname().split('.')[-1]

config = {
    # Consumer stuff
    "fmn.consumer.enabled": True,
    "fmn.sqlalchemy.uri": "sqlite:////var/tmp/fmn-dev-db.sqlite",

    # Backend stuff
    "fmn.email.mailserver": "127.0.0.1:25",
    "fmn.email.from_address": "fedmsg-notifications@fedoraproject.org",

    # Generic stuff
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
