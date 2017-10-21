=============
Configuration
=============

.. automodule:: fmn.config
    :members:


The Database
============

FMN uses `Alembic`_ to manage its database migrations. Additionally, FMN provides a
``fmn-createdb`` command to create the initial database.


Services
========

FMN provides a number of services.


FedMsg Consumer
---------------

FMN provides a `fedmsg consumer`_ which can be run by the ``fedmsg-hub`` service. This service
subscribes to the ZeroMQ publishing sockets and dispatches `Celery`_ tasks to determine what
users are interested in notifications. These tasks are sent to `Celery workers`_ via RabbitMQ.


fmn-celerybeat
--------------

``fmn-celerybeat`` is a `Celery beat`_ service that dispatches periodic tasks that are handled
by the Celery workers.


fmn-worker
----------

``fmn-worker`` is a Celery worker service. You can run an arbitrary number of these workers on
multiple hosts. They need to be able to access RabbitMQ, Redis, and the database. Once it
determines who should receive notifications, it sends messages to the "backends" message queue.


fmn-backend
-----------

``fmn-backend`` is a Twisted application that handles the actual delivery of the notifications.
It subscribes to the "backends" AMQP message queue. You should only run one instance of this
service.


.. _Alembic: http://alembic.zzzcomputing.com/en/latest/
.. _Celery: http://docs.celeryproject.org/en/latest/
.. _Celery beat: http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html
.. _Celery workers: http://docs.celeryproject.org/en/latest/userguide/workers.html
.. _fedmsg consumer: https://fedmsg.readthedocs.io/en/stable/subscribing/
