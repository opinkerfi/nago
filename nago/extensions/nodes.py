# -*- coding: utf-8 -*-

""" Management around connected nodes """

import nago.core
from nago.core import nago_access
import nago.settings
import socket

@nago_access(name='list')
def list_nodes(search="unsigned"):
    """ List all connected nodes
    """
    nodes = nago.core.get_nodes()
    if search == "all":
        return nodes
    elif search == 'unsigned':
        result = {}
        for token, node in nodes.items():
            if node.get('access') is None:
                result[token] = node
        return result
    else:
        result = {}
        for token, node in nodes.items():
            host_name = node.get('host_name')
            if search in (token, host_name):
                result[token] = node
        return result

@nago_access()
def add(node_name, **kwargs):
    """ Create a new node and generate a token for it """
    result = {}
    kwargs = kwargs.copy()
    overwrite = kwargs.pop('overwrite', False)
    node = nago.core.get_node(node_name)
    if not node:
        node = nago.core.Node()
    elif not overwrite:
        result['status'] = 'error'
        result['message'] = "node %s already exists. add argument overwrite=1 to overwrite it." % (node_name)
        return result
    else:
        node.delete()
        node = nago.core.Node()
    node['host_name'] = node_name
    for k, v in kwargs.items():
        node[k] = v
    node.save()
    result['message'] = "node successfully saved"
    result['node_data'] = node.data
    return result

@nago_access()
def delete(node_name):
    """ Delete a specific node """
    result = {}
    node = nago.core.get_node(node_name)
    if not node:
        result['status'] = 'error'
        result['message'] = "node not found."
    else:
        node.delete()
        result['status'] = 'success'
        result['message'] = 'node deleted.'
    return result

@nago_access()
def sign(node=None):
    """ Sign a specific node to grant it access

     you can specify "all" to sign all nodes

     returns the nodes that were signed
    """
    if not node:
        raise Exception("Specify either 'all' your specify token/host_name of node to sign. ")
    if node == 'all':
        node = 'unsigned'
    nodes = list_nodes(search=node)
    result = {}
    for token, i in nodes.items():
        i['access'] = 'node'
        i.save()
        result[token] = i
    return result

@nago_access(name='set')
def set_attribute(token_or_hostname, **kwargs):
    """ Change the attributes of a connected node """
    node = nago.core.get_node(security_token) or {}
    if not kwargs:
        return "No changes made"
    for k, v in kwargs.items():
        node[k] = v
    node.save()
    return "Saved %s changes" % len(kwargs)

@nago_access(access_required="node")
def ping(token_or_hostname=None):
    """ Send an echo request to a nago host.

    Arguments:
        token_or_host_name  -- The remote node to ping
                            If node is not provided, simply return pong
                            You can use the special nodenames "server" or "master"
     """
    if not token_or_hostname:
        return "Pong!"
    node = nago.core.get_node(token_or_hostname)
    if not node and token_or_hostname in ('master', 'server'):
        token_or_hostname = nago.settings.get_option('server')
        node = nago.core.get_node(token_or_hostname)
    if not node:
        try:
            address = socket.gethostbyname(token_or_hostname)
            node = nago.core.Node()
            node['host_name'] = token_or_hostname
            node['address'] = address
            node['access'] = 'node'
            if token_or_hostname == nago.settings.get_option('server'):
                node['access'] = 'master'
            node.save()
        except Exception:
            raise Exception("'%s' was not found in list of known hosts, and does not resolve to a valid address" % token_or_hostname)
    return node.send_command('nodes', 'ping')

@nago_access()
def connect(remote_host):
    """ Connect to remote host and show our status """
    if remote_host in ('master', 'server'):
        remote_host = nago.settings.get_option('server')
    node = nago.core.get_node(remote_host)
    if not node:
        try:
            address = socket.gethostbyname(remote_host)
            node = nago.core.Node()
            node['host_name'] = remote_host
            node['address'] = address
            node['access'] = 'node'
            if token_or_hostname == nago.settings.get_option('server'):
                node['access'] = 'master'
            node.save()
        except Exception:
            raise Exception("'%s' was not found in list of known hosts, and does not resolve to a valid address" % remote_host)
    ping_result = node.send_command('nodes', 'ping')
    if 'Pong' in ping_result.get('result', ''):
        return "Connection with %s ok" % remote_host
    else:
        return ping_result.get('result', ping_result)

