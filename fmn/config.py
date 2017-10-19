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
"""
FMN uses `fedmsg's configuration`_ files to load its configuration. In order to
adjust the default configuration settings for FMN, you will need to adjust
the fedmsg configuration.


Available Configuration Keys
============================

.. _datanommer-sqlalchemy-url:

``datanommer.sqlalchemy.url``
    :class:`str`: The database URL.

    Default: ``None``

.. _datanommer-enabled:

``datanommer.enabled``
    :class:`bool`: If true, FMN will query datanommer for recent fedmsgs that match a
    user's preference.

    Default: ``False``

.. _fas-credentials:

``fas_credentials``
    :class:`dict`: A dictionary with 'username' and 'password' keys containing the
    Fedora Account System credentials to use.

    Default: ``{'username': None, 'password': None,}``

.. _fmn-web-default_login:

``fmn.web.default_login``
    :class:`str`: The location to redirect users to in order to authenticate.

    Default: ``"login"``

.. _fmn-web-theme_css_url:

``fmn.web.theme_css_url``
    :class:`str`: The URL to a CSS theme to use instead of the default theme.

    Default: ``None``

.. _fmn-sse-pika-host:

``fmn.sse.pika.host``
    :class:`str`: The hostname of the RabbitMQ server to connect to for SSE.

    Default: ``"localhost"``

.. _fmn-sse-pika-port:

``fmn.sse.pika.port``
    :class:`int`: The port the RabbitMQ server is listening on.

    Default: ``5672``

.. _fmn-sse-pika-msg_expiration:

``fmn.sse.pika.msg_expiration``
    :class:`int`: The amount of time in milliseconds SSE messages should remain
    queued before being deleted.

    Default: ``3600000``

.. _fmn-sse-webserver-tcp_port:

``fmn.sse.webserver.tcp_port``
    :class:`int`: The TCP port the SSE server should listen on.

    Default: ``8080``

.. _fmn-sse-webserver-interfaces:

``fmn.sse.webserver.interfaces``
    :class:`str`: A comma-separated list of interfaces for the SSE server to listen on
    (e.g. ``"127.0.0.1, 192.168.1.2"``).

    Default: ``None`` (All interfaces)

.. _fmn-sse-webserver-queue_whitelist:

``fmn.sse.webserver.queue_whitelist``
    :class:`str`: A regular expression that defines a set of valid AMQP queue names
    users can listen on via the SSE server.

    Default: ``None``

.. _fmn-sse-webserver-queue_blacklist:

``fmn.sse.webserver.queue_blacklist``
    :class:`str`: A regular expression that defines a set of AMQP queue names users
    cannot listen on via the SSE Server. The whitelist is applied before the blacklist.

    Default: ``None``

.. _fmn-sse-webserver-allow_origin:

``fmn.sse.webserver.allow_origin``
    :class:`str`: The value to place in the ``Access-Control-Allow-Origin`` header.

    Default: ``"*"``

.. _fmn-sse-webserver-prefetch_count:

``fmn.sse.webserver.prefetch_count``
    :class:`int`: The number of messages to pre-fetch from the AMQP server.A

    Default: 5

.. _fmn-topics:

``fmn.topics``
    :class:`str` or :class:`list`: The ZeroMQ message topics to subscribe to in
    the FMN consumer. For example, setting this to ``b'org.fedoraproject.prod'``
    will filter out all staging fedmsgs.

    Default: ``"*"``

.. _fmn-sqlalchemy-uri:

``fmn.sqlalchemy.uri``
    :class:`str`: The URI of the database to use for users and preferences.

    Default: ``'sqlite:////var/tmp/fmn-dev-db.sqlite'``

.. _fmn-sqlalchemy-debug:

``fmn.sqlalchemy.debug``
    :class:`bool`: When true, SQLAlchemy will be configured to emit the SQL statements
    it generates at the DEBUG log level.

    Default: ``False``

.. _fmn-autocreate:

``fmn.autocreate``
    :class:`bool`: When true, users will be automatically created in FMN when FAS
    accounts are created.

    Default: ``False``.

.. _ fmn-junk_suffixes:

``fmn.junk_suffixes``
    :class:`list`: A list of fedmsg topic suffixes to ignore.

    Default: ``[]``.

.. _ignored_copr_owners:

``ignored_copr_owners``
    :class:`list`: A list of COPR project owners to drop messages from.

    Default: ``[]``.

.. _fmn.rules.utils.use_pagure_for_ownership:

``fmn.rules.utils.use_pagure_for_ownership``
    :class:`bool`: If true, query Pagure for package ownership.

    Default: ``True``

.. _fmn.rules.utils.pagure_api_url:

``fmn.rules.utils.pagure_api_url``
    :class:`str`: The URL for the Pagure instance to query for package ownership.

    Default: ``"https://src.stg.fedoraproject.org/api/"``


.. _fmn.rules.utils.use_pkgdb2:

``fmn.rules.utils.use_pkgdb2``
    :class:`bool`: If true, use pkgdb2 for package ownership data.

    Default: ``False``

.. _fmn.rules.utils.pkgdb2_api_url:

``fmn.rules.utils.pkgdb2_api_url``
    :class:`str`: The URL for the pkgdb2 instance to query for package ownership.

    Default: ``None``

.. _fmn-rules-cache:

``fmn.rules.cache``
    :class:`dict`: A ``dogpile.cache`` configuration dictionary.

    Default::

        {
            'backend': 'dogpile.cache.redis',
            'arguments': {
                'host': 'localhost',
                'port': 6379,
                'db': 0,
                'redis_expiration_time': 7200,
                'distributed_lock': True
            }
        }

.. _fmn-backends:

``fmn.backends``
    :class:`list`: A list of backends that are enabled. Options are "irc", "email",
    and "sse".

    Default: ``['email', 'irc']``

.. _fmn-backends-debug:

``fmn.backends.debug``
    :class:`bool`: If true, replace all backends with a debugging backend that simply
    logs the message it would have sent.

    Default: ``False``

.. _fmn-email-mailserver:

``fmn.email.mailserver``
    :class:`str`: The mail server to use when sending emails. Specify in the format
    ``<hostname>:<port>``.

    Default: ``"127.0.0.1:25"``

.. _fmn-email-from_address:

``fmn.email.from_address``
    :class:`str`: The email address to use in the ``From`` header in email notifications.

    Default: ``"notifications@fedoraproject.org"``

.. _fmn-irc-network:

``fmn.irc.network``
    :class:`str`: The IRC network to connect to for IRC notifications.

    Default: ``"irc.freenode.net"``

.. _fmn-irc-nickname:

``fmn.irc.nickname``
    :class:`str`: The nickname to use when sending IRC notifications.

    Default: ``"fmndev"``

.. _fmn-irc-nickserv_pass:

``fmn.irc.nickserv_pass``
    :class:`str`: The IRC NickServ password to use when identifying with the given
    IRC network.

    Default: ``None``

.. _fmn-irc-port:

``fmn.irc.port``
    :class:`int`: The port to use when connecting to the IRC network.

    Default: ``6697``

.. _fmn-irc-use_ssl:

``fmn.irc.use_ssl``
    :class:`bool`: Whether or not to use TLS when connecting to the IRC network.

    Default: ``True``

.. _fmn-irc-timeout:

``fmn.irc.timeout``
    :class:`int`: The amount of time to wait before timing out when connecting to the
    IRC network.

    Default: ``120``

.. _fmn-sse-url:

``fmn.sse.url``
    :class:`str`: The URL to use when connecting to the SSE server.

    Default: ``"http://localhost:8080/``

.. _fmn-base_url:

``fmn.base_url``
    :class:`str`: The URL to use for the FMN web application.

    Default: ``"http://localhost:5000/``

.. _fmn-acceptance_url:

``fmn.acceptance_url``
    :class:`str`: The URL template to use for acceptance in confirmation messages.

    Default: ``http://localhost:5000/confirm/accept/{secret}'

.. _fmn-rejection_url:

``fmn.rejection_url``
    :class:`str`: The URL template to use for rejection in confirmation messages.

    Default: ``http://localhost:5000/confirm/reject/{secret}'``

.. _fmn-support_email:

``fmn.support_email``
    :class:`str`: The email to offer for support in notifications.

    Default: ``"notifications@fedoraproject.org"``

.. _celery:

``celery``
    :class:`dict`: The Celery configuration dictionary.

    Default::
        {
            'broker': 'amqp://',
            'include': ['fmn.tasks'],
            'accept_content': ['json'],
            'task_serializer': 'json',
            'task_default_queue': 'fmn.tasks.unprocessed_messages',
            'beat_schedule': {
                'process-digests': {
                    'task': 'fmn.tasks.batch_messages',
                    'schedule': 60.0,
                },
                'process-confirmations': {
                  'task': 'fmn.tasks.confirmations',
                  'schedule': 15.0,
                },
            },
        }

.. _logging:

``logging``
    :class:`dict`: The logging configuration dictionary.

    Default::

        {
            'version': 1,
            'formatters': {
                'bare': {
                    'datefmt': '%Y-%m-%d %H:%M:%S',
                    'format': '[%(asctime)s][%(name)10s %(levelname)7s] %(message)s'
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'bare',
                    'stream': 'ext://sys.stdout',
                },
            },
            'loggers': {
                'fmn': {
                    'level': 'INFO',
                    'propagate': False,
                    'handlers': ['console'],
                }
            },
            'root': {
                'level': 'WARNING',
                'handlers': ['console'],
            },
        }

.. _fedmsg's configuration: https://fedmsg.readthedocs.io/en/stable/configuration/
"""
import fedmsg
import six


def _validate_none_or_type(t):
    """
    Validate a setting is either None or a given type.

    Args:
        t: The type to assert.
    """
    def _validate(setting):
        """
        Check the setting to make sure it's the right type.

        Args:
            object: The setting to check.

        Returns:
            object: The unmodified object if it's the proper type.

        Raises:
            ValueError: If the setting is the wrong type.
        """
        if setting is not None and not isinstance(setting, t):
            raise ValueError('"{}" is not "{}"'.format(setting, t))
        return setting
    return _validate


class _FmnConfig(dict):
    """
    FMN configuration dictionary.

    Attributes:
        loaded (bool): Indicates whether the configuration files have been loaded.
    """

    loaded = False

    _defaults = {
        'datanommer.sqlalchemy.url': {
            'default': None,
            'validator': _validate_none_or_type(str),
        },
        'datanommer.enabled': {
            'default': False,
            'validator': bool,
        },
        'fas_credentials': {
            'default': {'username': None, 'password': None},
            'validator': dict,
        },
        'fmn.web.default_login': {
            'default': 'login',
            'validator': None,
        },
        'fmn.web.theme_css_url': {
            'default': None,
            'validator': None,
        },
        'fmn.sse.pika.host': {
            'default': 'localhost',
            'validator': None,
        },
        "fmn.sse.pika.port": {
            'default': 5672,
            'validator': int,
        },
        'fmn.sse.pika.msg_expiration': {
            'default': 3600000,  # 1 hour in ms
            'validator': int,
        },
        'fmn.sse.webserver.tcp_port': {
            'default': 8080,
            'validator': int,
        },
        'fmn.sse.webserver.interfaces': {
            'default': '',
            'validator': None,
        },
        'fmn.sse.webserver.queue_whitelist': {
            'default': None,
            'validator': None,
        },
        'fmn.sse.webserver.queue_blacklist': {
            'default': None,
            'validator': None,
        },
        'fmn.sse.webserver.allow_origin': {
            'default': '*',
            'validator': None,
        },
        'fmn.sse.webserver.prefetch_count': {
            'default': 5,
            'validator': None,
        },
        'fmn.topics': {
            'default': [b'*'],
            'validator': None,
        },
        'fmn.sqlalchemy.uri': {
            'default': 'sqlite:////var/tmp/fmn-dev-db.sqlite',
            'validator': str,
        },
        'fmn.sqlalchemy.debug': {
            'default': False,
            'validator': None,
        },
        'fmn.autocreate': {
            'default': False,
            'validator': bool,
        },
        'fmn.junk_suffixes': {
            'default': [],
            'validator': _validate_none_or_type(list),
        },
        'ignored_copr_owners': {
            'default': [],
            'validator': _validate_none_or_type(list),
        },
        'fmn.rules.utils.use_pagure_for_ownership': {
            'default': True,
            'validator': bool,
        },
        'fmn.rules.utils.pagure_api_url': {
            'default': 'https://src.stg.fedoraproject.org/api/',
            'validator': _validate_none_or_type(str),
        },
        'fmn.rules.utils.use_pkgdb2': {
            'default': False,
            'validator': bool,
        },
        'fmn.rules.utils.pkgdb2_api_url': {
            'default': None,
            'validator': _validate_none_or_type(str),
        },
        'fmn.rules.cache': {
            'default': {
                'backend': 'dogpile.cache.redis',
                'arguments': {
                    'host': 'localhost',
                    'port': 6379,
                    'db': 0,
                    'redis_expiration_time': 60 * 60 * 2,
                    'distributed_lock': True,
                },
            },
            'validator': None,
        },
        'irc_color_lookup': {
            'default': {
                'fas': 'light blue',
                'bodhi': 'green',
                'git': 'red',
                'tagger': 'brown',
                'wiki': 'purple',
                'logger': 'orange',
                'pkgdb': 'teal',
                'buildsys': 'yellow',
                'planet': 'light green',
                'fmn': 'purple',
            },
            'validator': None,
        },
        'fmn.backends': {
            'default': ['email', 'irc'],
            'validator': None,
        },
        'fmn.backends.debug': {
            'default': False,
            'validator': None,
        },
        'fmn.email.mailserver': {
            'default': '127.0.0.1:25',
            'validator': None,
        },
        'fmn.email.from_address': {
            'default': 'notifications@fedoraproject.org',
            'validator': None,
        },
        'fmn.irc.network': {
            'default': 'irc.freenode.net',
            'validator': None,
        },
        'fmn.irc.nickname': {
            'default': 'fmndev',
            'validator': None,
        },
        'fmn.irc.nickserv_pass': {
            'default': None,
            'validator': None,
        },
        'fmn.irc.port': {
            'default': 6697,
            'validator': int,
        },
        'fmn.irc.use_ssl': {
            'default': True,
            'validator': None,
        },
        'fmn.irc.timeout': {
            'default': 120,
            'validator': int,
        },
        'fmn.sse.url': {
            'default': 'http://localhost:8080/',
            'validator': None,
        },
        'fmn.base_url': {
            'default': 'http://localhost:5000/',
            'validator': None,
        },
        'fmn.acceptance_url': {
            'default': 'http://localhost:5000/confirm/accept/{secret}',
            'validator': None,
        },
        'fmn.rejection_url': {
            'default': 'http://localhost:5000/confirm/reject/{secret}',
            'validator': None,
        },
        'fmn.support_email': {
            'default': 'notifications@fedoraproject.org',
            'validator': None,
        },
        'celery': {
            'default': {
                'broker': 'amqp://',
                'include': ['fmn.tasks'],
                'accept_content': ['json'],
                'task_serializer': 'json',
                'task_default_queue': 'fmn.tasks.unprocessed_messages',
                'beat_schedule': {
                    'process-digests': {
                        'task': 'fmn.tasks.batch_messages',
                        'schedule': 60.0,
                    },
                    'process-confirmations': {
                      'task': 'fmn.tasks.confirmations',
                      'schedule': 15.0,
                    },
                },
            },
            'validator': None,
        },
        'logging': {
            'default': {
                'version': 1,
                'formatters': {
                    'bare': {
                        'datefmt': '%Y-%m-%d %H:%M:%S',
                        'format': '[%(asctime)s][%(name)10s %(levelname)7s] %(message)s'
                    },
                },
                'handlers': {
                    'console': {
                        'class': 'logging.StreamHandler',
                        'formatter': 'bare',
                        'stream': 'ext://sys.stdout',
                    },
                },
                'loggers': {
                    'fmn': {
                        'level': 'INFO',
                        'propagate': False,
                        'handlers': ['console'],
                    }
                },
                'root': {
                    'level': 'WARNING',
                    'handlers': ['console'],
                },
            },
            'validator': None,
        },
    }

    def __getitem__(self, *args, **kw):
        """Load the default configuration if necessary otherwise proxy to :class:`dict`"""
        if not self.loaded:
            self.load_config()
        return super(_FmnConfig, self).__getitem__(*args, **kw)

    def get(self, *args, **kw):
        """Load the default configuration if necessary otherwise proxy to :class:`dict`"""
        if not self.loaded:
            self.load_config()
        return super(_FmnConfig, self).get(*args, **kw)

    def pop(self, *args, **kw):
        """Load the default configuration if necessary otherwise proxy to :class:`dict`"""
        if not self.loaded:
            self.load_config()
        return super(_FmnConfig, self).pop(*args, **kw)

    def copy(self, *args, **kw):
        """Load the default configuration if necessary otherwise proxy to :class:`dict`"""
        if not self.loaded:
            self.load_config()
        return super(_FmnConfig, self).copy(*args, **kw)

    def load_config(self, settings=None):
        """
        Load the configuration either from the config file, or from the given settings.

        args:
            settings (dict): If given, the settings are pulled from this dictionary. Otherwise, the
                config file is used.
        """
        self._load_defaults()
        if settings:
            self.update(settings)
        else:
            self.update(fedmsg.config.load_config())
        self.loaded = True
        self._validate()

    def _load_defaults(self):
        """Iterate over self._defaults and set all default values on self."""
        for k, v in self._defaults.items():
            self[k] = v['default']

    def _validate(self):
        """Run the validators found in self._defaults on all the corresponding values."""
        errors = []
        for k in self._defaults.keys():
            try:
                validator = self._defaults[k]['validator']
                if validator is not None:
                    self[k] = validator(self[k])
            except ValueError as e:
                errors.append(u'\t{}: {}'.format(k, six.text_type(e)))

        if errors:
            raise ValueError(
                u'Invalid config values were set: \n{}'.format(u'\n'.join(errors)))


#: The application configuration dictionary.
app_conf = _FmnConfig()
