# -*- coding: utf-8 -*-

""" Run local nagios plugins """

import nago.core
from nago.core import nago_access
import nago.settings
import os.path
import pynag.Utils
import subprocess

@nago_access()
def get(search="unsigned"):
    """ List all available plugins"""
    plugins = []
    for i in os.walk('/usr/lib/nagios/plugins'):
        for f in i[2]:
            plugins.append(f)
    return plugins

@nago_access()
def run(plugin_name, *args, **kwargs):
    """ Run a specific plugin """
    plugindir = nago.settings.get_option('plugin_dir')
    plugin = plugindir + "/" + plugin_name
    if not os.path.isfile(plugin):
        raise ValueError("Plugin %s not found" % plugin)

    command = [plugin] + list(args)
    p = subprocess.Popen(command, stdout=subprocess.PIPE,stderr=subprocess.PIPE,)
    stdout, stderr = p.communicate('through stdin to stdout')
    result = {}
    result['stdout'] = stdout
    result['stderr'] = stderr
    result['return_code'] = p.returncode
    return result



