# -*- coding: utf-8 -*-
""" Extension for the facter command

This extension allows getting facts (via 'facter' command) about this host,

posting facts is also supported, which means the agent will store facts about a remote server in memory.

"""

from nago.core import nago_access
from nago.core import get_nodes
import nago
import nago.extensions.settings
import nago.extensions.info
import json
facts = {}
from pynag.Utils import runCommand

@nago_access()
def get():
    """ Get local facts about this machine.

    Returns:
        json-compatible dict with all facts of this host
    """
    result = runCommand('facter --json', raise_error_on_fail=True)
    json_facts = result[1]
    facts = json.loads(json_facts)
    return facts

@nago_access(access_required="node")
def post(host_token, **kwargs):
    """ Store facts about a remote host in memory.

    Facts will be stored in nago.extensions.facts with the remote token as a key

    """
    nago.extensions.info.node_data[host_token]['facts'] = kwargs
    return "thanks!"


@nago_access()
def get_all():
    """ Get all facts about all nodes """
    result = {}
    for k,v in nago.extensions.info.node_data.items():
        result[k] = v.get('facts', {})
    return result

@nago_access()
def send(remote_host=None):
    """ Send my facts to a remote host

    if remote_host is provided, data will be sent to that host. Otherwise it will be sent to master.
    """
    my_facts = get()
    if not remote_host:
        remote_host = nago.extensions.settings.get('server')
    remote_node = nago.core.get_node(remote_host)
    if not remote_node:
        raise Exception("Remote host with token='%s' not found" % remote_host)
    response = remote_node.send_command('facts', 'post', host_token=remote_node.token, **my_facts)
    result = {}
    result['server_response'] = response
    result['message'] = "sent %s facts to remote node '%s'" % (len(my_facts), remote_node.get('host_name'))
    return result

