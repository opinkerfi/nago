# -*- coding: utf-8 -*-

""" Management around connected peers """

import nago.core
from nago.core import nago_access

@nago_access
def master(uri, **kwargs):
    """ Connect to a remote nago instance and mark it as an agent """
    return nago.core.get_peers()


@nago_access
def master(uri, **kwargs):
    """ Connect to a remote nago instance and mark it as an agent """
    return nago.core.get_peers()

