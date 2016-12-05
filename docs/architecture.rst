
FMN Architecture
================

This describes the various components of FMN and their architecture.

System Diagram
--------------

The general workflow is as follows::

                                                       +-------------+
                                                Read   |             |   Write
                                                +------+  prefs DB   +<------+
                                                |      |             |       |
     +                                          |      +-------------+       |
     |                                          |                            |   +------------------+   +--------+
     |                                          |                            |   |    |fmn.lib|     |   |        |
     |                                          v                            |   |    +-------+     |<--+  User  |
     |                                    +----------+                       +---+                  |   |        |
     |                                    |   fmn.lib|                           |  Central WebApp  |   +--------+
     |                                    |          |                           +------------------+
     |                             +----->|  Worker  +--------+
     |                             |      |          |        |
  fedmsg                           |      +----------+        |
     |                             |                          |
     |                             |      +----------+        |
     |   +------------------+      |      |   fmn.lib|        |       +--------------------+
     |   | fedmsg consumer  |      |      |          |        |       | Backend            |
     +-->|                  +------------>|  Worker  +--------------->|                    |
     |   |                  |      |      |          |        |       +-----+   +---+  +---+
     |   +------------------+      |      +----------+        |       |email|   |IRC|  |SSE|
     |                             |                          |       +--+--+---+-+-+--+-+-+
     |                             |      +----------+        |          |        |      |
     |                             |      |   fmn.lib|        |          |        |      |
     |                             |      |          |        |          |        |      |
     |                             +----->|  Worker  +--------+          |        |      |
     |                         RabbitMQ   |          |    RabbitMQ       |        |      |
     |                                    +----------+                   |        |      |
     |                                                                   v        v      v
     |
     |
     |
     v


Database
--------

It is recommended that you use PostgreSQL for your database. The database
schema can be seen below:

.. figure:: images/database.png
   :align:  center

   Database schema.
