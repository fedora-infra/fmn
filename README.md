# FMN Server-Sent Events

FMN is a family of systems to manage end-user notifications triggered by
fedmsg, the Federated Message bus.

The FMN Server-Sent Events server allows users to view their fedmsg feed in realtime
using [server-sent events](https://html.spec.whatwg.org/multipage/comms.html#server-sent-events).
It relies on a service to populate the RabbitMQ message queues for it. Typically, this is
done with the FMN core services.

## Install

To get ``fmn.sse`` directly from PyPi you can use pip:

```
pip install fmn.sse
```

If you're using Fedora, you can install it with DNF:

```
sudo dnf install python-fmn-sse
```

If you're using CentOS 7, you can install it from EPEL 7 with yum:

```
sudo yum install python-fmn-sse
```

## Development Environment

To set up the development environment, you can either use Vagrant to provision
a virtual machine and automatically configure it, or you can manually set up
the environment.

### Vagrant

The easiest way to get a development environment set up is with Vagrant. Refer
to the [fmn repository](https://github.com/fedora-infra/fmn) for the Vagrantfile
and instructions on how to set up Vagrant.


### Manual

1. Install the system dependencies. For Fedora:
```
sudo dnf install python python-devel python3-devel python-virtualenvwrapper \
rabbitmq-server python-pip gcc libffi-devel openssl-devel zeromq-devel
```

2. Install the Python dependencies:
```
pip install -r requirements.txt
```

3. Install the ``fmn.sse`` package:
```
pip install -e .
```

## Running

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

## Test Data

```
workon sse-py2
pip install pytz
python dev-data.py
```

## Manual Testing

`sse_webserver.py` curl seems to work okay for me `curl http://localhost:8080/user/bob`

and/or

open up `sse_test_subscriber.html` in a browser and look at the JS console

## Running unittests
```
workon sse-py2
python setup.py test
```

with coverage

```
workon sse-py2
pip install -r requirements-test.txt
py.test --cov=fmn tests/
```

### Common issues

Q: I can't connect to rabbitmq with pika

A: Make sure you are running rabbitmq `sudo systemctl start rabbitmq-server`

Q: I get the following error
```
pika.exceptions.ChannelClosed: (406, "PRECONDITION_FAILED - inequivalent arg 'x-message-ttl' for queue 'skrzepto.id.fedoraproject.org' in vhost '/': received '60000' but current is '86400000'")
```

A: You have set the queue a ttl that is not the same. You need to either match the ttl or delete the queue and retry.

Go into http://localhost:15672/  and delete the queue. Thats assuming you enabled the management plugin https://www.rabbitmq.com/management.html

Q: Nothing is being displayed on the curl

A: Wait a few more seconds, it takes a moment to display the data. If it's more
than a minute check to see if the queue has data via the web ui http://localhost:15672/
