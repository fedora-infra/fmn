from fmn.lib.hinting import hint, prefixed as _


@hint(topics=[_('planet.post.new')])
def planet_post_new(config, message):
    """ New blog posts on the Fedora Planet

    Yes, yes.. you could always use an RSS reader... but if you add *this* rule
    to your filter, you'll get notifications when new posts appear on the
    `Fedora Planet <https://planet.fedoraproject.org>`_.
    """
    return message['topic'].endswith('planet.post.new')
