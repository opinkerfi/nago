# -*- coding: utf-8 -*-
__version__ = 0.1

from pynag.Parsers import mk_livestatus, config
import time
import os
import os.path
import tempfile
import ConfigParser
import pwd

def get_peers():
    """ Returns all peers in a list of dicts format
    """
    cfg_file = "/etc/nago/nago.ini"
    config = ConfigParser.ConfigParser()
    config.read(cfg_file)
    result = {}
    for token in config.sections():
        peer = {}
        for key, value in config.items(token):
            peer[key] = value
        result[token] = peer
    return result


def get_peer(token):
    all_peers = get_peers()
    return all_peers[token]




def get_version():
    """ Returns the current nago version """
    return __version__