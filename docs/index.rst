.. FMN documentation master file, created by
   sphinx-quickstart on Mon Dec  5 10:39:51 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

FedMSG Notifications
====================

Table of Contents:

.. toctree::
   :maxdepth: 2

   contributing
   architecture
   glossary


FedMSG Notifications is a family of systems built to manage end-user
notifications triggered by `fedmsg <http://fedmsg.com>`_, the FEDerated
MeSsaGe bus.

It offers a diverse set of notification media including (but not limited to)
email, Internet Relay Chat (IRC), and Server-Sent Events (SSE). Users can
configure their notification preferences for all these media in a single place.


Usage
-----

In a nutshell, here's the way this application works:

- You login and set up some preferences here, in this webapp.
- Events occur in Fedora Infrastructure and are broadcast over fedmsg.
- This application receives those events and compares them against your
  preferences. If there's a match, then it forwards you a notification.

We maintain a `lot of applications <https://apps.fedoraproject.org>`_. Over
time, there has been an initiative to get them all speaking a similar language
on the backend with fedmsg. Take a look at the `list of fedmsg topics
<http://fedmsg.com/en/latest/topics/>`_ to see what all is covered.

Get Involved
============

You can report `issues
<https://github.com/fedora-infra/fmn/issues>`_ and find the
`source <https://github.com/fedora-infra/fmn/>`_ on github.
The development team hangs out in ``#fedora-apps``. Please do stop by and say
hello.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

