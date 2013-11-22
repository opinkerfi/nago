# -*- coding: utf-8 -*-
""" Extension for the facter command

This extension allows getting facts (via 'facter' command) about this host,

posting facts is also supported, which means the agent will store facts about a remote server in memory.

"""

from nago.core import nago_access
from nago.core import get_peers
import json
facts = {}
from pynag.Utils import runCommand

@nago_access
def get():
    """ Get local facts about this machine.

    Returns:
        json-compatible dict with all facts of this host
    """
    result = runCommand('facter --json', raise_error_on_fail=True)
    json_facts = result[1]
    facts = json.loads(json_facts)
    return facts

@nago_access
def post(host_token, **kwargs):
    """ Store facts about a remote host in memory.

    Facts will be stored in nago.extensions.facts with the remote token as a key

    """
    facts[host_token] = kwargs
    return "thanks!"


@nago_access
def get_all():
    """ Get all facts about all nodes """
    return facts

@nago_access
def send(remote_host=None):
    """ Send my facts to a remote host

    if remote_host is provided, data will be sent to that host. Otherwise it will be sent to master.
    """
    my_facts = get()
    remote_peer = None  # Here we will store the Peer we connect to

    for token, i in get_peers().items():
        if token == remote_host:
            remote_peer = i
            break
        elif remote_host is None and i.get('access') == 'master':
            remote_peer = i
            break
    if not remote_peer:
        raise Exception("Remote host with token='%s' not found" % remote_host)
    result = remote_peer.send_command('facts', 'post', host_token=remote_peer.token, **my_facts)
    return "sent %s facts to remote peer '%s'" % (len(my_facts), remote_peer.token)




if __name__ == '__main__':
    my_facts = get_facts()
    post_facts("123", my_facts)

    print facts



