from gettext import gettext as _
import logging.config

from fedmsg import config as fedmsg_config
from twisted.application import internet, service
from twisted.web import server

from fmn.sse.server import SSEServer


app_config = fedmsg_config.load_config()


logging.config.dictConfig(app_config.get('logging'))
_log = logging.getLogger('fmn.sse')
_log.info('Successfully configured logging for the SSE Server')


# Configure the twisted application itself.
application = service.Application(_('FMN Server Sent Events Server'))
site = server.Site(SSEServer())
service_collection = service.IServiceCollection(application)

port = app_config.get('fmn.sse.webserver.tcp_port', 8080)
interfaces = app_config.get('fmn.sse.webserver.interfaces')

if interfaces:
    for interface in interfaces.split(','):
        i = internet.TCPServer(int(port), site, interface=interface.strip())
        i.setServiceParent(service_collection)
    _log.info(_('SSE server is listening to port {0} on the {1} '
                'interfaces').format(port, interfaces))
else:
    # If not defined, listen on all interfaces
    i = internet.TCPServer(int(port), site)
    i.setServiceParent(service_collection)
    _log.info(_('SSE server is listening to port {0} on all available '
                'interfaces').format(port))
