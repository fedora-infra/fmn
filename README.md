#FMN.SSE

FMN is a family of systems to manage end-user notifications triggered by
fedmsg, the Fedora Federated Message bus.

FMN.SSE allows fedora users to view their fedmsg feed in realtime.

## Install
System dependencies
```
sudo yum install python python-devel python-virtualenvwrapper rabbitmq-server \
python-pip gcc libffi-devel openssl-devel zeromq-devel
```

If running with python2
```
mkvirtualenv sse-py2
workon sse-py2
pip install -r requirements.txt
```

For python3

*replace sse-py2 for sse-py3 in other notes*
```
sudo dnf install python3-devel
mkvirtualenv --python=/usr/bin/python3 sse-py3
workon sse-py3
pip install -r requirements.txt
```

## Running

```
sudo systemctl start rabbitmq-server
workon sse-py2
PYTHONPATH=. python fmn/sse/sse_webserver.py
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

