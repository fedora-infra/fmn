#FMN.SSE

## Install
```
mkvirtualenv sse
workon sse
pip install -r ./requirements.txt
```

## Running

There are two files `sse-webserver.py` and `sse-server.py`

```
workon sse
python sse-webserver.py
```

## Manual Testing

`sse-webserver.py` curl seems to work okay for me `curl http://localhost:8080`

`sse-server` telnet  `telnet localhost 1234` then hit enter once it asks you which you want to join

### Common issues

Q: I can't connect to rabbitmq

A: Make sure you are running rabbitmq `sudo systemctl start rabbitmq-server`

Q: I get the following error
```
pika.exceptions.ChannelClosed: (406, "PRECONDITION_FAILED - inequivalent arg 'x-message-ttl' for queue 'skrzepto.id.fedoraproject.org' in vhost '/': received '60000' but current is '86400000'")
```

A: You have set the queue a ttl that is not the same. You need to either match the ttl or delete the queue and retry.

Go into http://localhost:15672/  and delete the queue. Thats assuming you enabled the management plugin https://www.rabbitmq.com/management.html


