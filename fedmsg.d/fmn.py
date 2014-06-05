import socket
hostname = socket.gethostname().split('.')[-1]


config = {
    # Consumer stuff
    "fmn.consumer.enabled": True,
    "fmn.sqlalchemy.uri": "sqlite:////var/tmp/fmn-dev-db.sqlite",

    # Our web frontend also needs to be able to talk to datanommer to get
    # example messages that match rules (optional)
    "datanommer.sqlalchemy.url": "postgresql+psycopg2://datanommer:bunbunbun@localhost:5432/datanommer",

    # Some configuration for the rule processors
    "fmn.rules.utils.use_pkgdb2": False,
    "fmn.rules.utils.pkgdb2_api_url": "http://209.132.184.188/api/",
    "fmn.rules.cache": {
        "backend": "dogpile.cache.dbm",
        "expiration_time": 300,
        "arguments": {
            "filename": "/var/tmp/fmn-cache.dbm",
        },
    },

    ## Backend stuff ##

    # This is the list of enabled backends (so we can turn one off globally)
    #"fmn.backends": ['email', 'irc', 'android'],
    "fmn.backends": ['email', 'irc'],

    # Email
    "fmn.email.mailserver": "127.0.0.1:25",
    "fmn.email.from_address": "notifications@fedoraproject.org",

    # IRC
    "fmn.irc.network": "irc.freenode.net",
    "fmn.irc.nickname": "pingoubot",
    "fmn.irc.port": 6667,
    "fmn.irc.timeout": 120,

    # GCM - Android notifs
    "fmn.gcm.post_url": "wat",
    "fmn.gcm.api_key": "wat",

    # Confirmation urls:
    "fmn.base_url": "http://localhost:5000/",
    "fmn.acceptance_url": "http://localhost:5000/confirm/accept/{secret}",
    "fmn.rejection_url": "http://localhost:5000/confirm/reject/{secret}",
    "fmn.support_email": "notifications@fedoraproject.org",

    # Generic stuff
    "endpoints": {
        "fmn.%s" % hostname: [
            "tcp://127.0.0.1:3041",
            "tcp://127.0.0.1:3042",
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
