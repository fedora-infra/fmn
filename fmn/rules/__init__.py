from fmn.rules.ansible import *
from fmn.rules.askbot import *
from fmn.rules.bodhi import *
from fmn.rules.generic import *
from fmn.rules.pkgdb import *


def DevelopmentFilter(*args, **kwargs):
    """ All messages

    This lets every message through not matter the content.

    (Useful for development)
    """
    return True
