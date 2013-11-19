
import time
import os
import os.path
import tempfile
import ConfigParser
import pwd

from pynag.Parsers import mk_livestatus, config

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

    print("{level}: {message}".format(**locals()))


def nago_access(func):
    """ Decorate other functions with this one to allow access """
    func.nago_access = True
    return func


def get_peers():
    """ Returns all peers in a list of dicts format
    """
    cfg_file = "/etc/nago/nago.ini"
    config = ConfigParser.ConfigParser()
    config.read(cfg_file)
    result = {}
    for token in config.sections():
        peer = {}
        for key, value in config.items(token):
            peer[key] = value
        result[token] = peer
    return result


def get_peer(token):
    all_peers = get_peers()
    return all_peers[token]

