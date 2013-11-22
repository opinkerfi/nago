# -*- coding: utf-8 -*-

""" Management around connected peers """

import nago.core
from nago.core import nago_access

@nago_access
def list(search="unsigned"):
    """ List all connected peers
    """
    peers = nago.core.get_peers()
    if search == "all":
        return peers
    elif search == 'unsigned':
        result = {}
        for token, peer in peers.items():
            if peer.get('access') is None:
                result[token] = peer
        return result
    else:
        result = {}
        for token, peer in peers.items():
            host_name = peer.get('host_name')
            if search in (token, host_name):
                result[token] = peer
        return result

@nago_access
def sign(node=None):
    """ Sign a specific node to grant it access

     you can specify "all" to sign all nodes

     returns the nodes that were signed
    """
    if not node:
        raise Exception("Specify either 'all' your specify token/host_name of node to sign. ")
    if node == 'all':
        node = 'unsigned'
    nodes = list(search=node)
    result = {}
    for token, i in nodes:
        i['access'] = 'node'
        i.save()
        result[token] = i
    return result

@nago_access
def set(token_or_hostname, **kwargs):
    """ Change the attributes of a connected peer """
    peer = nago.core.get_peer(security_token) or {}
    if not kwargs:
        return "No changes made"
    for k, v in kwargs.items():
        peer[k] = v
    peer.save()
    return "Saved %s changes" % len(kwargs)

