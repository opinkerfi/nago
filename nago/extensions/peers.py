# -*- coding: utf-8 -*-

""" Management around connected peers """

import nago.core
from nago.core import nago_access

@nago_access
def get():
    """ List all connected peers
    """
    return nago.core.get_peers()

@nago_access
def edit(security_token, **kwargs):
    """ Change the attributes of a connected peer """
    peer = nago.core.get_peer(security_token) or {}
    if not kwargs:
        return "No changes made"
    for k, v in kwargs.items():
        peer[k] = v
    peer.save()
    return "Saved %s changes" % len(kwargs)