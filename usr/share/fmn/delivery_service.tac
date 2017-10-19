# vi: set ft=python :
#
# This file is part of the FMN project.
# Copyright (C) 2017 Red Hat, Inc.
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

from twisted.application import service

from fmn import config
from fmn.delivery.service import DeliveryService


logging.config.dictConfig(config.app_conf['logging'])
_log = logging.getLogger('fmn.delivery.service')
_log.info('Successfully configured logging for the FMN Delivery Service')


# Configure the twisted application itself.
application = service.Application(_('FMN Delivery Service'))
service = DeliveryService()
service.setServiceParent(application)
