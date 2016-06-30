from FeedQueue import FeedQueue
from datetime import datetime
from random import randint

number_messages = 1000

fq = FeedQueue()
for i in range(number_messages):
    msg = "time is: " + str(datetime.now().time()) + \
          "  here's a random number: " + str(randint(0, i))
    fq.push_message(msg)

print 'finished pushing messages'
