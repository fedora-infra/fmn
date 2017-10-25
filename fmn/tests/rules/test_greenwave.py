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
"""Tests for the :mod:`fmn.rules.greenwave` module."""
from __future__ import unicode_literals

import copy

from fmn.rules import greenwave
from fmn.tests import Base


GREENWAVE_MSG = {
    "username": "openshift",
    "i": 59,
    "timestamp": 1508934768.0,
    "msg_id": "2017-db45b07c-b39a-4fd3-af49-ae7cb83bb78b",
    "crypto": "x509",
    "topic": "org.fedoraproject.prod.greenwave.greenwave.decision.update",
    "msg": {
        "policies_satisified": False,
        "decision_context": "bodhi_update_push_stable",
        "product_version": "fedora-27",
        "applicable_policies": [
            "taskotron_release_critical_tasks_for_stable",
            "taskotron_release_critical_tasks_for_stable_with_blacklist"
        ],
        "unsatisfied_requirements": [
            {
                "testcase": "dist.abicheck",
                "item": {
                    "item": "lilypond-doc-2.19.80-1.fc25",
                    "type": "koji_build"
                },
                "type": "test-result-missing"
            }
        ],
        "subject": [
            {
                "item": "lilypond-doc-2.19.80-1.fc25",
                "type": "koji_build"
            }
        ],
        "summary": "1 of 3 required tests not found",
        "previous": {
            "policies_satisified": False,
            "summary": "2 of 3 required tests not found",
            "unsatisfied_requirements": [
                {
                    "testcase": "dist.upgradepath",
                    "item": {
                        "item": "lilypond-doc-2.19.80-1.fc25",
                        "type": "koji_build"
                    },
                    "type": "test-result-missing"
                },
                {
                    "testcase": "dist.abicheck",
                    "item": {
                        "item": "lilypond-doc-2.19.80-1.fc25",
                        "type": "koji_build"
                    },
                    "type": "test-result-missing"
                }
            ],
            "applicable_policies": [
                "taskotron_release_critical_tasks_for_stable",
                "taskotron_release_critical_tasks_for_stable_with_blacklist"
            ]
        }
    }
}


class TestGreenwaveDecisionUpdate(Base):
    '''Test greenwave_decision_update()'''

    def test_topic_match(self):
        '''Correct topic must match'''
        self.assertTrue(greenwave.greenwave_decision_update(
            self.config, GREENWAVE_MSG))

    def test_topic_no_match(self):
        '''Different topic must not match'''
        msg = copy.deepcopy(GREENWAVE_MSG)
        msg['topic'] = "org.fedoraproject.prod.some.other.service"
        self.assertFalse(greenwave.greenwave_decision_update(
            self.config, msg))

        msg = copy.deepcopy(GREENWAVE_MSG)
        msg['topic'] = "org.fedoraproject.prod.fakegreenwave.decision.update"
        self.assertFalse(greenwave.greenwave_decision_update(
            self.config, msg))
