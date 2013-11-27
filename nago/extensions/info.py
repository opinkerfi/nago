# -*- coding: utf-8 -*-

""" Collect and transmit information about local node """

import nago.core
from nago.core import nago_access
import nago.protocols.httpserver
import nago.extensions.settings
import unittest

node_data = {}

@nago_access()
def get_info(node_name=None, key=None):
    """ Get information about this node """
    if node_name is None:
        node_name = nago.core.get_my_info()['host_name']
    data = node_data.get(node_name, {})
    if not key:
        return data
    else:
        return data.get(key)



@nago_access()
def post(node_name, key, data):
    """ Give the server information about this node

    Arguments:
        node -- node_name or token for the node this data belongs to
        key  -- identifiable key, that you use later to retrieve that piece of data
        data -- the data you need to store

    """
    node = node_data.get(node_name, {})
    node[key] = data
    node_data[node_name] = node
    return "thanks!"


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