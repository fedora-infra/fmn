import json
import uuid
from datetime import datetime as dt
from random import randint
import pytz
import six
from fmn.sse.FeedQueue import FeedQueue


def create_fake_message(additional_text=''):
    dom_id = six.text_type(uuid.uuid4())

    output = {"dom_id": str(dom_id),
              "date_time": dt.utcnow().replace(
                  tzinfo=pytz.utc).isoformat(),
              "icon": "https://seccdn.libravatar.org/avatar/"
                      "ba1882fd5522d16213b0535934f77b796f0b89f76edd65460078099"
                      "fe97c20ea?s=64&d=retro",
              "link": "localhost:8080",
              "markup": "New message added to the queue.\t" + additional_text,
              "secondary_icon": "https://secure.gravatar.com/avatar/"
                                "ba1882fd5522d16213b0535934f77b796f0b89f76edd"
                                "65460078099fe97c20ea.jpg?s=64&d"
              }

    return json.dumps(output)


def push_data(fq, number_messages=1000):
    for i in range(number_messages):
        msg = "time is: " + str(dt.now().time()) + \
              "  here's a random number: " + str(randint(0, i))
        formatted_message = create_fake_message(msg)
        fq.push_message(formatted_message)


fq = FeedQueue(queue_name='skrzepto.id.fedoraproject.org', exchange='user')
push_data(fq)
fq = FeedQueue(queue_name='bob.id.fedoraproject.org', exchange='user')
push_data(fq)

print('finished pushing messages')
