============
Installation
============

FMN is available on Fedora, `PyPI`_, and may also be available in your distribution's
repositories.

FMN depends on several services to work properly:

* `RabbitMQ`_, an AMQP message broker, used by Celery and the delivery service.

* `Redis`_, used for caching between worker processes.

* `PostgreSQL`_, used to store user notification preferences.

* `Datanommer`_, used to provide users with sample messages that match their preferences.


Fedora
======

FMN is packaged for Fedora::

  $ sudo dnf install python2-fmn rabbitmq-server redis postgresql-server

Optionally, you can install `Flower`_ to monitor the tasking system.


.. _Datanommer: https://github.com/fedora-infra/datanommer
.. _Flower: https://flower.readthedocs.io/
.. _PostgreSQL: https://www.postgresql.org/
.. _PyPI: https://pypi.org/project/fmn/
.. _RabbitMQ: https://www.rabbitmq.com/
.. _Redis: https://redis.io/
