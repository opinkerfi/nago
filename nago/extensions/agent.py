# -*- coding: utf-8 -*-

""" Manage settings on a local node """

# this is a workaround for rhel6 systems where python-jinja has multiple versions
# installed at the same time
# https://bugzilla.redhat.com/show_bug.cgi?id=867105
__requires__ = ['jinja2 >= 2.4']
import pkg_resources

import nago.core
from nago.core import nago_access
import nago.protocols.httpserver
import unittest

@nago_access()
def start(debug=False, host='127.0.0.1'):
    """ starts a nago agent (daemon) process """
    if debug:
        debug = True
    nago.protocols.httpserver.app.run(debug=debug, host=host)


@nago_access()
def stop(key, section='main'):
    """ stops the nago agent
    """
    pass

