======================
FMN Server-Sent Events
======================

The FMN Server-Sent Events server allows users to view their fedmsg feed in realtime
using [server-sent events](https://html.spec.whatwg.org/multipage/comms.html#server-sent-events).
It relies on a service to populate the RabbitMQ message queues for it. Typically, this is
done with the FMN core services.

Running
=======

1. Ensure RabbitMQ is running:
```
sudo systemctl start rabbitmq-server
```

2. Start the SSE server:
```
twistd -n -l - -y usr/share/fmn.sse/server.tac
```

3. Make sure the server is available. This should return a HTTP 404:
```
curl -v http://localhost:8080/
```

Test Data
=========

::
  $ pip install pytz
  $ python dev-data.py

Common issues
=============

Q: I can't connect to rabbitmq with pika

A: Make sure you are running rabbitmq `sudo systemctl start rabbitmq-server`

Q: I get the following error

::
  pika.exceptions.ChannelClosed: (406, "PRECONDITION_FAILED - inequivalent arg 'x-message-ttl' for queue 'skrzepto.id.fedoraproject.org' in vhost '/': received '60000' but current is '86400000'")

A: You have set the queue a ttl that is not the same. You need to either match the ttl or delete the queue and retry.

Go into http://localhost:15672/  and delete the queue. Thats assuming you enabled the management plugin https://www.rabbitmq.com/management.html

Q: Nothing is being displayed on the curl

A: Wait a few more seconds, it takes a moment to display the data. If it's more
than a minute check to see if the queue has data via the web ui http://localhost:15672/
