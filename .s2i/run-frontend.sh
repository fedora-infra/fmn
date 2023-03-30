#!/bin/bash

# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

mkdir /httpdir/run
ln -s /etc/httpd/modules /httpdir/modules
truncate --size=0 /httpdir/accesslog /httpdir/errorlog
tail -qf /httpdir/accesslog /httpdir/errorlog &
exec httpd -f /opt/app-root/src/.s2i/httpd.conf -DFOREGROUND -DNO_DETACH
