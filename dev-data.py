import json
import uuid
from datetime import datetime
from random import randint

import six
from faker import Factory

from fmn.sse.FeedQueue import FeedQueue

fake = Factory.create()


def creat_fake_message(additional_text=''):
    dom_id = six.text_type(uuid.uuid4())
    fake_date = fake.date_time_between(start_date='-7y', end_date='-1')

    output = {"dom_id": str(dom_id),
              "human_time": str(fake_date),
              "icon": str('icon'),
              "link": str('localhost:8080'),
              "markup": str(
                  'New message added to the queue.    ' + additional_text),
              "secondary_icon": str('Secondary icon')
              }

    return json.dumps(output)


def push_data(fq, number_messages=1000):
    for i in range(number_messages):
        msg = "time is: " + str(datetime.now().time()) + \
              "  here's a random number: " + str(randint(0, i))
        formatted_message = creat_fake_message(msg)
        fq.push_message(formatted_message)


fq = FeedQueue(queue_name='skrzepto.id.fedoraproject.org', exchange='user')
push_data(fq)
fq = FeedQueue(queue_name='bob.id.fedoraproject.org', exchange='user')
push_data(fq)

print 'finished pushing messages'
