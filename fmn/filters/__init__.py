from fmn.filters.ansible import *
from fmn.filters.askbot import *
from fmn.filters.bodhi import *
from fmn.filters.generic import *
from fmn.filters.pkgdb import *


def DevelopmentFilter(*args, **kwargs):
    """ All messages

    This lets every message through not matter the content.

    (Useful for development)
    """
    return True
