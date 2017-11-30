# This file is part of the FMN project.
# Copyright (C) 2017 Red Hat, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""Tests for the :mod:`fmn.delivery.backends.mail` module."""
from twisted.mail import smtp
import mock

from fmn.lib import models, defaults
from fmn.delivery.backends import mail
from fmn.tests import Base


class EmailBackendTests(Base):

    @mock.patch('fmn.delivery.backends.mail.get_fas_email',
                mock.Mock(return_value='invalid@fedoraproject.org'))
    @mock.patch('fmn.delivery.backends.mail.smtp.sendmail',
                mock.Mock(side_effect=smtp.SMTPClientError(550, 'boop')))
    def test_deliver_550_matching_email(self):
        """
        Assert when email fails with 550 and the email set matches FAS, the preference is
        disabled.
        """
        user = models.User(
            openid='jcline.id.fedoraproject.org', openid_url='http://jcline.id.fedoraproject.org')
        self.sess.add(user)
        context = models.Context(
            name='email', description='description', detail_name='email', icon='wat')
        self.sess.add(context)
        self.sess.commit()
        defaults.create_defaults_for(
            self.sess, user,
            detail_values={'email': 'invalid@fedoraproject.org'})
        self.sess.commit()
        preference = models.Preference.query.filter_by(
            context_name='email', openid='jcline.id.fedoraproject.org').first()
        preference.enabled = True
        self.sess.add(preference)
        self.sess.commit()
        config = {
            'fmn.email.mailserver': 'localhost:25',
            'fmn.email.from_address': 'nobody@example.com',
        }
        backend = mail.EmailBackend(config)
        recipient = {
            'email address': 'invalid@fedoraproject.org',
            'user': 'jcline',
        }

        backend.deliver('my mail', recipient, {})

        preference = models.Preference.query.filter_by(
            context_name='email', openid='jcline.id.fedoraproject.org').first()
        self.assertFalse(preference.enabled)

    @mock.patch('fmn.delivery.backends.mail.get_fas_email',
                mock.Mock(return_value='valid@fedoraproject.org'))
    @mock.patch('fmn.delivery.backends.mail.smtp.sendmail',
                mock.Mock(side_effect=smtp.SMTPClientError(550, 'boop')))
    def test_deliver_550_new_email(self):
        """
        Assert when email fails with 550 and the email set doesn't match FAS,
        the preference is updated with the new email.
        """
        user = models.User(
            openid='jcline.id.fedoraproject.org', openid_url='http://jcline.id.fedoraproject.org')
        self.sess.add(user)
        context = models.Context(
            name='email', description='description', detail_name='email', icon='wat')
        self.sess.add(context)
        self.sess.commit()
        defaults.create_defaults_for(
            self.sess, user,
            detail_values={'email': 'invalid@fedoraproject.org'})
        self.sess.commit()
        preference = models.Preference.query.filter_by(
            context_name='email', openid='jcline.id.fedoraproject.org').first()
        preference.enabled = True
        self.sess.add(preference)
        self.sess.commit()
        config = {
            'fmn.email.mailserver': 'localhost:25',
            'fmn.email.from_address': 'nobody@example.com',
        }
        backend = mail.EmailBackend(config)
        recipient = {
            'email address': 'invalid@fedoraproject.org',
            'user': 'jcline',
        }

        backend.deliver('my mail', recipient, {})

        preference = models.Preference.query.filter_by(
            context_name='email', openid='jcline.id.fedoraproject.org').first()
        self.assertTrue(preference.enabled)
        self.assertEqual(u'valid@fedoraproject.org', preference.detail_values[0].value)
