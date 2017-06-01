# Copyright (c) 2011-2016 Mike Bayer
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author or contributors may not be used to endorse or
#    promote products derived from this software without specific prior
#    written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
"""A backport of the kwarg_function_key_generator in dogpile.cache 0.6.2."""

import inspect


def kwarg_function_key_generator(namespace, fn, to_str=str):
    """Return a function that generates a string
    key, based on a given function as well as
    arguments to the returned function itself.

    For kwargs passed in, we will build a dict of
    all argname (key) argvalue (values) including
    default args from the argspec and then
    alphabetize the list before generating the
    key.

    .. versionadded:: 0.6.2

    .. seealso::

        :func:`.function_key_generator` - default key generation function

    """

    if namespace is None:
        namespace = '%s:%s' % (fn.__module__, fn.__name__)
    else:
        namespace = '%s:%s|%s' % (fn.__module__, fn.__name__, namespace)

    argspec = inspect.getargspec(fn)
    default_list = list(argspec.defaults or [])
    # Reverse the list, as we want to compare the argspec by negative index,
    # meaning default_list[0] should be args[-1], which works well with
    # enumerate()
    default_list.reverse()
    # use idx*-1 to create the correct right-lookup index.
    args_with_defaults = dict((argspec.args[(idx*-1)], default)
                              for idx, default in enumerate(default_list, 1))
    if argspec.args and argspec.args[0] in ('self', 'cls'):
        arg_index_start = 1
    else:
        arg_index_start = 0

    def generate_key(*args, **kwargs):
        as_kwargs = dict(
            [(argspec.args[idx], arg)
             for idx, arg in enumerate(args[arg_index_start:],
                                       arg_index_start)])
        as_kwargs.update(kwargs)
        for arg, val in args_with_defaults.items():
            if arg not in as_kwargs:
                as_kwargs[arg] = val

        argument_values = [as_kwargs[key]
                           for key in sorted(as_kwargs.keys())]
        return namespace + '|' + " ".join(map(to_str, argument_values))
    return generate_key
