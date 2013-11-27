# -*- coding: utf-8 -*-

""" Manage settings on a local node """

import ConfigParser
from nago.core import nago_access


@nago_access(name='set')
def edit_settings(section='main', **kwargs):
    """ Change a single option in local configuration """
    cfg_file = "/etc/nago/nago.ini"
    config = ConfigParser.ConfigParser()
    config.read(cfg_file)
    for k, v in kwargs.items():
        config.set(section=section, option=k, value=v)
    with open(cfg_file, 'w') as f:
        config.write(f)
    return "Done"


@nago_access(name='get')
def get(key, section='main'):
    """ Get a single option from """
    cfg_file = "/etc/nago/nago.ini"
    config = ConfigParser.ConfigParser()
    config.read(cfg_file)
    return config.get(section, key)
