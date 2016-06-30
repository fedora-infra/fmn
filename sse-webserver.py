import json
import urllib2
from twisted.internet import interfaces, reactor, defer, task
from FeedQueue import FeedQueue
from twisted.web import server, resource
from twisted.internet import reactor


def get_recent_posts():
    delta = "delta=86400"  # one day worth of data
    rows_per_page = "rows_per_page=50"
    url = "https://apps.fedoraproject.org/datagrepper/raw" + "?" + delta + "&" + rows_per_page
    request = urllib2.Request(url)
    contents = urllib2.urlopen(request).read()
    json_response = json.loads(contents)
    return json_response['raw_messages']


class Simple(resource.Resource):
    isLeaf = True
    #TODO: Add routes to inividual pages
    # eg.  /group/<groupname>   /user/<username>
    def render_GET(self, request):
        request.responseHeaders.addRawHeader(b"content-type",
                                             b"application/json")
        self.write_messages(request)
        lc = task.LoopingCall(self.write_messages, request)
        lc.start(2)  # this seems to not react fast enough after the client has closed and keeps running
        # seperate thread???
        #reactor.callLater(10, request.finish)
        return server.NOT_DONE_YET

    def write_messages(self, request):
        fq = FeedQueue()
        data = fq.receive_one_message()
        request.write(data)

site = server.Site(Simple())
reactor.listenTCP(8080, site)
reactor.run()

