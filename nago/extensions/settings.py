# -*- coding: utf-8 -*-

""" Manage settings on a local node """

import nago.core
import ConfigParser
from nago.core import nago_access

@nago_access
def set(section='main', **kwargs):
    """ Change a single option in local configuration """
    cfg_file = "/etc/nago/nago.ini"
    config = ConfigParser.ConfigParser()
    config.read(cfg_file)
    for k, v in kwargs.items():
        config.set(section=section, option=k, value=v)
    with open(cfg_file,'w') as f:
        config.write(f)
    return "Done"


@nago_access
def get(key, section='main'):
    """ Get a single option from """
    cfg_file = "/etc/nago/nago.ini"
    config = ConfigParser.ConfigParser()
    config.read(cfg_file)
    return config.get(section, key)
