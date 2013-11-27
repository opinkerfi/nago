# -*- coding: utf-8 -*-

""" Run local nagios plugins """

import nago.core
from nago.core import nago_access
import nago.extensions.settings
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
def run(plugin, *args, **kwargs):
    """ Run a specific plugin """
    plugin = '/usr/lib/nagios/plugins/' + plugin
    # todo: make sure plugin is inside plugindir
    command = [plugin] + list(args)
    p = subprocess.Popen(command, stdout=subprocess.PIPE,stderr=subprocess.PIPE,)
    stdout, stderr = p.communicate('through stdin to stdout')
    result = {}
    result['stdout'] = stdout
    result['stderr'] = stderr
    result['return_code'] = p.returncode
    return result



@nago_access()
def set(token_or_hostname, **kwargs):
    """ Change the attributes of a connected node """
    node = nago.core.get_node(security_token) or {}
    if not kwargs:
        return "No changes made"
    for k, v in kwargs.items():
        node[k] = v
    node.save()
    return "Saved %s changes" % len(kwargs)

@nago_access()
def connect(token_or_hostname=None):
    """ Connect to another node. By default connect to the masternode """
    if token_or_hostname is None:
        token_or_hostname = nago.extensions.settings.get('server')
    node = nago.core.get_node(token_or_hostname)
    if not node:
        try:
            address = socket.gethostbyname(token_or_hostname)
            node = nago.core.Node()
            node['host_name'] = token_or_hostname
            node['address'] = address
        except Exception:
            raise Exception("'%s' was not found in list of known hosts, and does not resolve to a valid address" % token_or_hostname)
    node.send_command('nodes', 'list')
