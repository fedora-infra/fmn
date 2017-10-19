# -*- coding: utf-8 -*-
# vi: set ft=python :
#
# Copyright (C) 2017 Jeremy Cline
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.

from gettext import gettext as _
import logging.config

from twisted.application import internet, service
from twisted.web import server

from fmn.sse.server import SSEServer
from fmn import config


logging.config.dictConfig(config.app_conf['logging'])
_log = logging.getLogger('fmn.sse')
_log.info('Successfully configured logging for the SSE Server')


# Configure the twisted application itself.
application = service.Application(_('FMN Server Sent Events Server'))
site = server.Site(SSEServer())
service_collection = service.IServiceCollection(application)

port = config.app_conf['fmn.sse.webserver.tcp_port']
interfaces = config.app_conf['fmn.sse.webserver.interfaces']

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
