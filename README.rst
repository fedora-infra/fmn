fmn.lib
=======

`fmn <https://github.com/fedora-infra/fmn>`_ is a family of systems to manage
end-user notifications triggered by
`fedmsg, the Fedora FEDerated MESsage bus <http://fedmsg.com>`_.

This module contains the internal API components and data model for Fedora
Notifications

There is a parental placeholder repo with some useful information you might
want to read through, like an `overview
<https://github.com/fedora-infra/fmn/#fedora-notifications>`_, a little
`architecture diagram <https://github.com/fedora-infra/fmn/#architecture>`_.


HACKING
-------

Find development instructions here: https://github.com/fedora-infra/fmn/#hacking

To run the test suite, make sure you have `fmn.rules
<https://github.com/fedora-infra/fmn.rules>`_ checked out.
Then cd into fmn/lib/tests, and run nosetests.
If you have fmn.rules installed in a virtual environment,
make sure you also run nosetests from the same venv.
