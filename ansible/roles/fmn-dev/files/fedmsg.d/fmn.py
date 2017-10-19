import socket
hostname = socket.gethostname().split('.')[0]


config = {
    # Consumer stuff
    "fmn.consumer.enabled": True,

    # Our web frontend also needs to be able to talk to datanommer to get
    # example messages that match rules (optional)
    "datanommer.sqlalchemy.url": "postgresql+psycopg2://datanommer@localhost:5432/datanommer",
    'datanommer.enabled': True,
}
