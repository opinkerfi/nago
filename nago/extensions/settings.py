# -*- coding: utf-8 -*-

""" Manage settings on a local node """

import nago.settings
from nago.core import nago_access


@nago_access(name='set')
def edit_settings(section='main', **kwargs):
    """ Change a single option in local configuration """
    return nago.settings.set_option(section, **kwargs)


@nago_access(name='get')
def get(key, section='main'):
    """ Get a single option from """
    return nago.settings.get_option(option_name=key, section_name=section)