import socket
hostname = socket.gethostname().split('.')[0]


config = {
    # Consumer stuff
    "fmn.consumer.enabled": True,
    "datanommer.enabled": False,
    "fmn.sqlalchemy.uri":  "postgresql://postgres:anypasswordworkslocally@localhost/notifications",
}
