# -*- coding: utf-8 -*-
#
# This file is part of FMN.
# Copyright (C) 2017 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Suite 500, Boston, MA 02110-1335,  USA

from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('greenwave.decision.update')])
def greenwave_decision_update(config, message, **kwargs):
    """ Greenwave decisions

    This rule lets through messages from the `greenwave
    <https://fedoraproject.org/wiki/Infrastructure/Factory2/Focus/Greenwave>`_
    gating system about new decisions.
    """
    return message['topic'].endswith('.greenwave.decision.update')
