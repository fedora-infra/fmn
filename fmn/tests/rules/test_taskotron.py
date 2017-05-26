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
"""Tests for the :mod:`fmn.rules.taskotron` module."""
from __future__ import unicode_literals

import copy

from fmn.rules import taskotron
from fmn.tests import Base


RPMLINT_MSG = {
    "source_name": "datanommer",
    "i": 2255,
    "timestamp": 1496047851.0,
    "msg_id": "2017-131442a4-0c4b-4bca-bb20-c8d8809e994b",
    "topic": "org.fedoraproject.prod.taskotron.result.new",
    "source_version": "0.7.0",
    "msg": {
        "task": {
          "item": "perl-PAR-Packer-1.037-1.fc27",
          "type": "koji_build",
          "name": "dist.rpmlint"
        },
        "result": {
          "prev_outcome": None,
          "outcome": "PASSED",
          "id": 14280446,
          "submit_time": "2017-05-29 08:50:51 UTC",
          "log_url": "https://taskotron.fedoraproject.org/artifacts/"
                     "all/c40473a0-444b-11e7-b258-5254008e42f6/"
                     "task_output/perl-PAR-Packer-1.037-1.fc27.log"
        }
    }
}


def swap_outcome(outcome):
    '''For a given outcome, return a different one'''
    return 'FAILED' if outcome == 'PASSED' else 'PASSED'


class TestTaskotronResultNew(Base):
    '''Test taskotron_result_new()'''

    def setUp(self):
        super(TestTaskotronResultNew, self).setUp()
        self.msg = copy.deepcopy(RPMLINT_MSG)

    def test_topic_match(self):
        '''Correct topic must match'''
        self.assertTrue(taskotron.taskotron_result_new(
            self.config, self.msg))

    def test_topic_no_match(self):
        '''Different topic must not match'''
        self.msg['topic'] = "org.fedoraproject.prod.some.other.service"
        self.assertFalse(taskotron.taskotron_result_new(
            self.config, self.msg))

        self.msg['topic'] = "org.fedoraproject.prod.faketaskotron.result.new"
        self.assertFalse(taskotron.taskotron_result_new(
            self.config, self.msg))


class TestTaskotronTask(Base):
    '''Test taskotron_task()'''

    def setUp(self):
        super(TestTaskotronTask, self).setUp()
        self.msg = copy.deepcopy(RPMLINT_MSG)

    def test_exact_match(self):
        '''Match exactly task name'''
        task = self.msg['msg']['task']['name']
        self.assertTrue(taskotron.taskotron_task(
            self.config, self.msg, task))

    def test_no_match(self):
        '''Match exactly task name'''
        task = 'this_task_doesnt_exist'
        self.assertFalse(taskotron.taskotron_task(
            self.config, self.msg, task))

    def test_empty_task(self):
        '''Don't match empty task name'''
        task = ''
        self.assertFalse(taskotron.taskotron_task(
            self.config, self.msg, task))

        task = None
        self.assertFalse(taskotron.taskotron_task(
            self.config, self.msg, task))

    def test_case_insensitive(self):
        '''Matching should not be case sensitive'''
        task = self.msg['msg']['task']['name'].upper()
        self.assertTrue(taskotron.taskotron_task(
            self.config, self.msg, task))

        task = self.msg['msg']['task']['name'].lower()
        self.assertTrue(taskotron.taskotron_task(
            self.config, self.msg, task))

        task = self.msg['msg']['task']['name'].capitalize()
        self.assertTrue(taskotron.taskotron_task(
            self.config, self.msg, task))

    def test_splitting(self):
        '''Multiple values can be split with a comma. Handle extra
        whitespace.'''
        for suffix in [',',
                       ', ',
                       ' ,',
                       ',some.other.task',
                       ', some.other.task',
                       ' ,some.other.task']:
            task = self.msg['msg']['task']['name'] + suffix
            self.assertTrue(taskotron.taskotron_task(
                self.config, self.msg, task))

        for prefix in [',',
                       ', ',
                       ' ,',
                       'some.other.task,',
                       'some.other.task, ',
                       'some.other.task ,']:
            task = self.msg['msg']['task']['name'] + suffix
            self.assertTrue(taskotron.taskotron_task(
                self.config, self.msg, task))

        task = 'no.match1,no.match2'
        self.assertFalse(taskotron.taskotron_task(
            self.config, self.msg, task))

    def test_wildcards(self):
        '''Wildcards must work'''
        # == a star ==
        task = self.msg['msg']['task']['name'] + '*'
        self.assertTrue(taskotron.taskotron_task(
            self.config, self.msg, task))

        task = '*'
        self.assertTrue(taskotron.taskotron_task(
            self.config, self.msg, task))

        task = self.msg['msg']['task']['name'][:-1] + '*'
        self.assertTrue(taskotron.taskotron_task(
            self.config, self.msg, task))

        task = self.msg['msg']['task']['name'] + '*'
        self.msg['msg']['task']['name'] = \
            self.msg['msg']['task']['name'] + '.subtask'
        self.assertTrue(taskotron.taskotron_task(
            self.config, self.msg, task))

        task = 'no.match*'
        self.assertFalse(taskotron.taskotron_task(
            self.config, self.msg, task))

        # == a question mark ==
        task = self.msg['msg']['task']['name'] + '?'
        self.assertFalse(taskotron.taskotron_task(
            self.config, self.msg, task))

        task = self.msg['msg']['task']['name'][:-1] + '?'
        self.assertTrue(taskotron.taskotron_task(
            self.config, self.msg, task))

        # == a range ==
        task = self.msg['msg']['task']['name'][:-1] + '[a-z]'
        self.assertTrue(taskotron.taskotron_task(
            self.config, self.msg, task))

        task = self.msg['msg']['task']['name'][:-1] + '[!a-z]'
        self.assertFalse(taskotron.taskotron_task(
            self.config, self.msg, task))

    def test_wildcards_splitting(self):
        '''Wildcards must work when values are split'''
        task = self.msg['msg']['task']['name'] + '*,other.task'
        self.assertTrue(taskotron.taskotron_task(
            self.config, self.msg, task))

        task = 'other.task,*'
        self.assertTrue(taskotron.taskotron_task(
            self.config, self.msg, task))


class TestTaskotronChangedOutcome(Base):
    '''Test taskotron_changed_outcome()'''

    def setUp(self):
        super(TestTaskotronChangedOutcome, self).setUp()
        self.msg = copy.deepcopy(RPMLINT_MSG)

    def test_no_previous(self):
        '''No match for no previous outcome'''
        self.assertFalse(taskotron.taskotron_changed_outcome(
            self.config, self.msg))

    def test_same_outcome(self):
        '''No match for the same outcome'''
        self.msg['msg']['result']['prev_outcome'] = \
            self.msg['msg']['result']['outcome']
        self.assertFalse(taskotron.taskotron_changed_outcome(
            self.config, self.msg))

    def test_changed_outcome(self):
        '''Match changed outcome'''
        prev_outcome = swap_outcome(self.msg['msg']['result']['outcome'])
        self.msg['msg']['result']['prev_outcome'] = prev_outcome
        self.assertTrue(taskotron.taskotron_changed_outcome(
            self.config, self.msg))


class TestTaskotronTaskOutcome(Base):
    '''Test taskotron_task_outcome()'''

    def setUp(self):
        super(TestTaskotronTaskOutcome, self).setUp()
        self.msg = copy.deepcopy(RPMLINT_MSG)

    def test_no_outcome(self):
        '''No match on empty requested outcome'''
        outcome = None
        self.assertFalse(taskotron.taskotron_task_outcome(
            self.config, self.msg, outcome))

        outcome = ''
        self.assertFalse(taskotron.taskotron_task_outcome(
            self.config, self.msg, outcome))

    def test_desired_outcome(self):
        '''Match when desired outcome is present'''
        outcome = self.msg['msg']['result']['outcome']
        self.assertTrue(taskotron.taskotron_task_outcome(
            self.config, self.msg, outcome))

    def test_undesired_outcome(self):
        '''No match when undesired outcome is present'''
        outcome = swap_outcome(self.msg['msg']['result']['outcome'])
        self.assertFalse(taskotron.taskotron_task_outcome(
            self.config, self.msg, outcome))

    def test_splitting(self):
        '''Multiple values can be specified delimited by a comma'''
        correct_outcome = self.msg['msg']['result']['outcome']
        other_outcome = swap_outcome(correct_outcome)
        outcome = correct_outcome + ',' + other_outcome
        self.assertTrue(taskotron.taskotron_task_outcome(
            self.config, self.msg, outcome))

        outcome = other_outcome + ',' + other_outcome
        self.assertFalse(taskotron.taskotron_task_outcome(
            self.config, self.msg, outcome))

        # handle extra whitespace
        outcome = correct_outcome + ' ,' + other_outcome
        self.assertTrue(taskotron.taskotron_task_outcome(
            self.config, self.msg, outcome))

        outcome = other_outcome + ', ' + correct_outcome
        self.assertTrue(taskotron.taskotron_task_outcome(
            self.config, self.msg, outcome))

    def test_case_insensitive(self):
        '''Values should be case-insensitive.'''
        outcome = self.msg['msg']['result']['outcome'].upper()
        self.assertTrue(taskotron.taskotron_task_outcome(
            self.config, self.msg, outcome))

        outcome = self.msg['msg']['result']['outcome'].lower()
        self.assertTrue(taskotron.taskotron_task_outcome(
            self.config, self.msg, outcome))

        outcome = self.msg['msg']['result']['outcome'].capitalize()
        self.assertTrue(taskotron.taskotron_task_outcome(
            self.config, self.msg, outcome))


class TestTaskotronTaskParticularOrChangedOutcome(Base):
    '''Test taskotron_task_particular_or_changed_outcome()'''

    def setUp(self):
        super(TestTaskotronTaskParticularOrChangedOutcome, self).setUp()
        self.msg = copy.deepcopy(RPMLINT_MSG)

    def test_desired_unchanged_outcome(self):
        '''Match when desired unchanged outcome is present'''
        outcome = self.msg['msg']['result']['outcome']
        self.msg['msg']['result']['prev_outcome'] = None
        self.assertTrue(taskotron.taskotron_task_particular_or_changed_outcome(
            self.config, self.msg, outcome))

    def test_undesired_changed_outcome(self):
        '''Match when undesired changed outcome is present'''
        outcome = swap_outcome(self.msg['msg']['result']['outcome'])
        self.msg['msg']['result']['prev_outcome'] = outcome
        self.assertTrue(taskotron.taskotron_task_particular_or_changed_outcome(
            self.config, self.msg, outcome))

    def test_desired_changed_outcome(self):
        '''Match when desired changed outcome is present'''
        outcome = self.msg['msg']['result']['outcome']
        prev_outcome = swap_outcome(self.msg['msg']['result']['outcome'])
        self.msg['msg']['result']['prev_outcome'] = prev_outcome
        self.assertTrue(taskotron.taskotron_task_particular_or_changed_outcome(
            self.config, self.msg, outcome))

    def test_undesired_unchanged_outcome(self):
        '''No match when undesired unchanged outcome is present'''
        outcome = swap_outcome(self.msg['msg']['result']['outcome'])
        self.msg['msg']['result']['prev_outcome'] = None
        self.assertFalse(taskotron.taskotron_task_particular_or_changed_outcome(
            self.config, self.msg, outcome))


class TestTaskotronReleaseCriticalTask(Base):
    '''Test taskotron_release_critical_task()'''

    def setUp(self):
        super(TestTaskotronReleaseCriticalTask, self).setUp()
        self.msg = copy.deepcopy(RPMLINT_MSG)

    def test_critical(self):
        '''Match critical tasks'''
        for task in taskotron.RELEASE_CRITICAL_TASKS:
            self.msg['msg']['task']['name'] = task
            self.assertTrue(taskotron.taskotron_release_critical_task(
                self.config, self.msg))

    def test_not_critical(self):
        '''Don't match non-critical tasks'''
        self.msg['msg']['task']['name'] = 'some.task'
        self.assertFalse(taskotron.taskotron_release_critical_task(
            self.config, self.msg))
