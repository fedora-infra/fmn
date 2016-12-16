"""
FMN uses rules to determine whether or not to dispatch a message. A filter is
composed of one or more rules. A rule is something like: "is a bodhi message"
or "pertains to a package owned by me." They are implemented as python functions.
The database model refers to them as ``fmn.rules:pertains_to_me`` or
``fmn.rules:is_a_bodhi_message``. They can optionally take arguments.

A user can have zero or more filters for a particular messaging context.

For example::

  User ---+-------------------------+------------------+
          |                         |                  |
          V                         V                  V
         Email                     IRC               Android
          |                         |                  |
          +--->Filter1               +--->Filter1        +----->Filter1
          |       |                        |                    |
          |       +-> is a koji build      +-> pertains to a    +-> pertains
          |       |   completed message        package owned        to the
          |       |                            by me                package
          |       +-> pertains to a package                         'nethack'
          |       |   owned by me
          |       |
          |       +-> does not pertain to
          |           package 'nethack'
          |
          +--->Filter2
                  |
                  +-> is a bodhi message
                  |
                  +-> pertains to a package
                      owned by 'lmacken'

If *all* the rules match for *any* filter in a given context, a notification
is deployed for that context.  In other words, the filters are OR'd together
and the rules that make up a filter are AND'd together.  If multiple contexts
have a filter that succeeds, notifications are deployed for all of those
contexts.
"""

from fmn.rules.anitya import *
from fmn.rules.ansible import *
from fmn.rules.askbot import *
from fmn.rules.autocloud import *
from fmn.rules.bodhi import *
from fmn.rules.bugzilla import *
from fmn.rules.buildsys import *
from fmn.rules.compose import *
from fmn.rules.coprs import *
from fmn.rules.faf import *
from fmn.rules.fas import *
from fmn.rules.fedbadges import *
from fmn.rules.fedimg import *
from fmn.rules.fedocal import *
from fmn.rules.fedora_elections import *
from fmn.rules.fedoratagger import *
from fmn.rules.fmn_notifications import *
from fmn.rules.generic import *
from fmn.rules.github import *
from fmn.rules.git import *
from fmn.rules.hotness import *
from fmn.rules.infragit import *
from fmn.rules.jenkins import *
from fmn.rules.kerneltest import *
from fmn.rules.koschei import *
from fmn.rules.logger import *
from fmn.rules.mailman import *
from fmn.rules.mdapi import *
from fmn.rules.meetbot import *
from fmn.rules.nagios import *
from fmn.rules.nuancier import *
from fmn.rules.pagure import *
from fmn.rules.pkgdb import *
from fmn.rules.planet import *
from fmn.rules.summershum import *
from fmn.rules.taskotron import *
from fmn.rules.trac import *
from fmn.rules.wiki import *
