
FedMSG Notifications Development Guide
======================================

FedMSG Notifications welcomes contributions! Our issue tracker is located on
`GitHub <https://github.com/fedora-infra/fmn/issues>`_.


Contribution Guidelines
-----------------------

When you make a pull request, a Fedora Infrastructure team member will review your
code. Please make sure you follow the guidelines below:


Code style
^^^^^^^^^^

We follow the `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ style guide for Python.
The test suite includes a test that enforces the required style, so all you need to do is
run the tests to ensure your code follows the style. If the unit test passes, you are
good to go!


Unit tests
^^^^^^^^^^

All unit tests must pass. All new code should have 100% test coverage.
Any bugfix should be accompanied by one or more unit tests to demonstrate the fix.
If you are unsure how to write unit tests for your code, we will be happy to help
you during the code review process.

You can run the unit tests by running ``tox`` in the root
of the repository.


Development environment
-----------------------

The development environment is set up using `Ansible <https://www.ansible.com/>`_. You can use
this to set up a development enviroment on any host, but only the Ansible playbook on hosts you
are willing to reprovision since it expects to own the host. It does things like write to
``~/.bashrc`` and ``/etc/motd``.

You are also  welcome to examine the Ansible playbook and set up your own development
environment however you see fit

Vagrant
^^^^^^^

The best way to set up a development enviroment is to use `Vagrant <https://vagrantup.com/>`_.
Vagrant provisions a new virtual machine and then runs the Ansible playbook on it automatically.
To get started, install Vagrant::

    $ sudo dnf install vagrant libvirt vagrant-libvirt vagrant-sshfs ansible

Next, clone the repository and configure your Vagrantfile::

    $ git clone https://github.com/fedora-infra/fmn.git
    $ cd fmn
    $ cp Vagrantfile.example Vagrantfile
    $ vagrant up
    $ vagrant reload
    $ vagrant ssh

.. note::
    Before you can start the services, you must populate ~/.fedmsg.d/fas_credentials.py with
    your Fedora Account System credentials.

You now have a functional development environment. The message of the day for the virtual machine
has some helpful tips, but the FMN service can be started in the virtual machine with::

    $ fstart

Log output is viewable with ``journalctl`` and you can navigate to http://localhost:5000/ to
view the web user interface.

Release guidelines
------------------

The FMN is released as RPM package in Fedora `fXX-infra <https://koji.fedoraproject.org/koji/search?terms=*infra&type=target&match=glob>`_
tag. Where XX means the Fedora version.

Step by step guide
^^^^^^^^^^^^^^^^^^

#. Update version in repository

   * docs/conf.py

   * setup.py

#. Update CHANGELOG.rst

#. Update python-fmn.spec

   * Update version

   * Add changelog to bottom (Only add devel changes, that are related to package itself)
     
#. Commit the changes

   ``git commit -m "Prep for vX.X.X"`` (Replace X.X.X with version you want to release)

#. Push the commit

   ``git push origin/develop``

#. Create tag

   ``git tag X.X.X`` (Replace X.X.X with version you want to release)

   Message of the tag: "Release X.X.X" (Replace X.X.X with version you want to release)

#. Push the tag

   ``git push --tags``

#. Do a release on `GitHub releases <https://github.com/fedora-infra/fmn/releases>`_

   Use the CHANGELOG.rst

   Add contributors (check the previous release) - find names in git log

#. Download the ``fmn-X.X.X.tar.gz`` from GitHub release

#. Put it in ``SOURCES`` directory

   Default is ``~/rpmbuild/SOURCES``

#. Build the SRPM

   ``rpmbuld -bs --define "dist .fcXX" python-fmn.spec`` (Replace XX with Fedora version)

#. Build the package in koji ``fXX-infra`` tag (XX means Fedora release)

   ``koji build fXX-infra ~/rpmbuild/SRPMS/python-fmn-X.X.X-1.fc35.src.rpm``
   (Replace XX with Fedora version you want to build for and X.X.X with the release
   you created by ``rpmbuild``)

The RPM is now available in Koji.
