# -*- coding: utf-8 -*-

""" Collect and transmit information about local node """

import nago.core
from nago.core import nago_access
import nago.protocols.httpserver
import nago.settings
import unittest
from collections import defaultdict

node_data = defaultdict(dict)

@nago_access()
def get(security_token=None, key=None):
    """ Get information about this node """
    if security_token is None:
        security_token = nago.core.get_my_info()['host_name']
    data = node_data.get(security_token, {})
    if not key:
        return data
    else:
        return data.get(key)

@nago_access()
def get_all():
    """ Return all information about all nodes """
    return node_data



@nago_access(access_required="node")
def post(node_name, key, **kwargs):
    """ Give the server information about this node

    Arguments:
        node -- node_name or token for the node this data belongs to
        key  -- identifiable key, that you use later to retrieve that piece of data
        kwargs -- the data you need to store
    """
    node = nago.core.get_node(node_name)
    if not node:
        raise ValueError("Node named %s not found" % node_name)
    token = node.token
    node_data[token] = node_data[token] or {}
    node_data[token][key] = kwargs
    return "thanks!"

@nago_access()
def send(node_name):
    """ Send our information to a remote nago instance

    Arguments:
        node -- node_name or token for the node this data belongs to
    """
    my_data = nago.core.get_my_info()
    if not node_name:
        node_name = nago.settings.get('server')
    node = nago.core.get_node(node_name)
    json_params = {}
    json_params['node_name'] = node_name
    json_params['key'] = "node_info"
    for k, v in my_data.items():
        nago.core.log("sending %s to %s" % (k, node['host_name']), level="notice")
        json_params[k] = v
    return node.send_command('info', 'post', node_name=node.token, key="node_info", **my_data)

def on_load():
    my_info = nago.core.get_my_info()
    post(node_name=my_info.get('host_name'), key="my_info", data=my_info)


class TestInfo(unittest.TestCase):
    """ Unit Tests for the info extension """
    def test_get_info(self):
        # Call on_load() to load local info to memory
        on_load()

        # Get our own basic info, double check nago version number
        results = get_info()
        version = results.get('my_info', {}).get('nago_version')
        self.assertEqual(nago.get_version(), version)

        # Try post some changes and see if we can fetch them back
        host_name = results.get('my_info', {}).get('host_name')
        key = 'test'
        data = 'test data'
        tmp = post(host_name, key, data)
        self.assertEqual('thanks!', tmp)

        # get the same data back, make sure it matches
        posted_data = get_info(host_name, key)
        self.assertEqual(data, posted_data)