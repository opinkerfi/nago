
import time
import os
import os.path
import tempfile
import ConfigParser
import pwd

import string
import ConfigParser
import json
import requests
import urllib

import platform
import nago
from functools import wraps
from pynag.Parsers import mk_livestatus, config
import socket

#import nago.extensions.info

# List of log entries since program start. Format should be:
# [{'timestamp':x, 'level': x, 'message'}]
_log_entries = []


def log(message, level="info"):
    """ Add a new log entry to the nago log.

    Arguments:
        level - Arbritrary string, levels should be syslog style (debug,log,info,warning,error)
        message - Arbritary string, the message that is to be logged.
    """
    now = time.time()
    entry = {}
    entry['level'] = level
    entry['message'] = message
    entry['timestamp'] = now
    _log_entries.append(entry)
#    if level not in ('debug', 'info'):
#        print("{level}: {message}".format(**locals()))


def nago_access(access_required="master", name=None):
    """ Decorate other functions with this one to allow access

    Arguments:
        nago_access -- Type of access required to call this function
                       By default only master is allowed to make that call

        nago_name   -- What name this function will have to remote api
                       Default is the same as the name of the function being
                       decorated.
    """
    def real_decorator(func):
        func.nago_access = access_required
        func.nago_name = name or func.__name__
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return real_decorator


def get_nodes():
    """ Returns all nodes in a list of dicts format
    """
    cfg_file = "/etc/nago/nago.ini"
    config = ConfigParser.ConfigParser()
    config.read(cfg_file)
    result = {}
    for section in config.sections():
        if section in ['main']:
            continue
        token = section
        node = Node(token)
        for key, value in config.items(token):
            node[key] = value
        result[token] = node
    return result


def get_node(token_or_hostname):
    for name, node in get_nodes().items():
        if token_or_hostname in (name, node.get('host_name'), node.get('address'), node.get('uri')):
            return node
    return None


def has_access(token):
    """ Returns true if specified token exists and is marked as "allowed" """
    node = get_node(token) or {}
    if node.get('access'):
        return True
    return False


def generate_token():
    """ Generate a new random security token.

     >>> len(generate_token()) == 50
     True

     Returns:
       string
    """
    length = 50
    stringset = string.ascii_letters + string.digits
    token = ''.join([stringset[i % len(stringset)] for i in [ord(x) for x in os.urandom(length)]])
    return token

def register_node(token, node_info, **kwargs):
        host_name = node_info.get('host_name', 'unknown')
        node = nago.core.Node(token, host_name=host_name, **kwargs)
        node.save()
        return node


class Node(object):
    """ Represents one specific node (another nago client) """
    def __init__(self, token=None, **kwargs):
        if not token:
            token = generate_token()
        self.data = kwargs.copy()
        self.token = token
        self._original_token = token

    def __getitem__(self, item):
        return self.data[item]

    def get(self, attribute, default=None):
        return self.data.get(attribute, default)

    def __setitem__(self, item, value):
        self.data[item] = value

    def delete(self):
        """ Delete this node from config files """
        cfg_file = "/etc/nago/nago.ini"
        config = ConfigParser.ConfigParser()
        config.read(cfg_file)
        result = {}
        token = self.data.pop("token", self.token)
        if token not in config.sections():
            raise Exception("Cannot find node in config. Delete aborted.")
        config.remove_section(self.token)
        with open(cfg_file, 'w') as f:
            return config.write(f)

    def save(self):
        """ Save this node (and all its attributes) to config """
        cfg_file = "/etc/nago/nago.ini"
        config = ConfigParser.ConfigParser()
        config.read(cfg_file)
        result = {}
        token = self.data.pop("token", self.token)
        if token != self._original_token:
            config.remove_section(self._original_token)
            config.add_section(token)

        if token not in config.sections():
            config.add_section(token)
        for key, value in self.data.items():
            config.set(token, key, value)
        for key, value in config.items(token):
            if key not in self.data:
                config.set(token, key, None)
        with open(cfg_file, 'w') as f:
            return config.write(f)

    def __str__(self):
        return self.data.__str__()

    def __repr__(self):
        return self.data.__repr__()

    def get_info(self, key=None):
        """ Return all posted info about this node """
        node_data = nago.extensions.info.node_data.get(self.token, {})
        if key is None:
            return node_data
        else:
            return node_data.get(key, {})

    def update_info(self, key, value):
        node_data = nago.extensions.info.node_data.get(self.token, {})
        node_data[key] = value
        nago.extensions.info.node_data[self.token] = node_data

    def send_command(self, extension_name, method_name, **kwargs):
        uri = self.get('uri')
        address = self.get('address')
        host_name = self.get('host_name')
        port = self.get('port') or 5000
        port = str(port)
        arguments = kwargs.copy()
        arguments['token'] = arguments.pop('token', self.token)
        arguments['about_me'] = json.dumps(get_my_info())

        if host_name and not address:
            address = socket.gethostbyname(host_name)

        if not uri and not address:
            raise Exception("We need either a remote address or uri to connect to node")
        elif not uri:
            uri = "http://{address}:{port}".format(**locals())

        uri += "/api/{extension_name}/{method_name}?".format(**locals())
        querystring = urllib.urlencode(arguments.items())

        uri += querystring
        log("Connecting to {uri}".format(**locals()), level="debug")
        try:
            r = requests.get(uri)
            content = r.content
            if r.status_code == 200:
                log(message="Successfully connected to %s" % uri, level="debug")
            elif r.status_code == 403:
                log(message="Access denied when connecting to %s" % uri, level="error")
            results = json.loads(content)
            return results
        except Exception, e:
            results = {}
            results['error'] = "Failed to connect to %s" % uri
            results['error_type'] = type(e)
            results['details'] = e
            results['status'] = 'error'
            return results


def get_my_info():
    """ Return general information about this node
    """
    result = {}
    result['host_name'] = platform.node()
    result['real_host_name'] = platform.node()
    result['dist'] = platform.dist()
    result['nago_version'] = nago.get_version()
    return result