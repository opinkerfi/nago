__author__ = 'palli'

from pynag.Parsers import mk_livestatus, config
import time
import os
import os.path
import tempfile
import ConfigParser
import pwd

c = config()
c.parse_maincfg()
check_result_path = c.get_cfg_value("check_result_path")

user = 'nagios'
(uid, gid) = pwd.getpwnam(user)[2:4]


def get_checkresults():
    """ Returns a list of all checkresults on local nagios server. Data is returned as a list of statuses.
    """
    livestatus = mk_livestatus()
    hosts = livestatus.get_hosts()
    services = livestatus.get_services()
    result = {}
    result['hosts'] = hosts
    result['services'] = services
    return result


def post_checkresults(hosts=None, services=None):
    """
    Arguments:
      data     -- list of dicts,
    """
    fd, filename = tempfile.mkstemp(prefix='c', dir=check_result_path)
    if not hosts:
        hosts = []
    if not services:
        services = []
    checkresults = '### Active Check Result File Made by Nago ###\n'
    checkresults += 'file_time=%s' % (int(time.time()))
    checkresults += "\n"
    checkresults = ''
    with open(filename, 'w') as f:
        for host in hosts:
            checkresults += _format_checkresult(**host)
        for service in services:
            checkresults += _format_checkresult(**service)
        f.write(checkresults)
    #os.close(fd)
    os.chmod(filename, 0644)
    file('%s.ok' % filename, 'w')


def _format_checkresult(**kwargs):
    """ Returns a string in a nagios "checkresults" compatible format


    """
    o = {}
    o['check_type'] = '1'
    o['check_options'] = '0'
    o['scheduled_check'] = '1'
    o['reschedule_check'] = '1'
    o['latency'] = '0.0'
    o['start_time'] = '%5f' % time.time()
    o['finish_time'] = '%5f' % time.time()
    o['early_timeout'] = '0'
    o['exited_ok'] = '1'
    o['long_plugin_output'] = ''
    o['performance_data'] = ''
    o.update(locals())
    o.update(kwargs)
    del o['kwargs']
    del o['o']

    template = _host_check_result
    # Escape all linebreaks if we have them
    for k, v in o.items():
        if isinstance(v, basestring) and '\n' in v:
            o[k] = v.replace('\n', '\\n')

    # Livestatus returns slightly different output than status.dat
    # Lets normalize everything to status.dat format
    if 'name' in o and not 'host_name' in o:
        o['host_name'] = o['name']
    if 'state' in o and not 'return_code' in o:
        o['return_code'] = o['state']
    if 'description' in o and not 'service_description' in o:
        o['service_description'] = o['description']
    if not o['performance_data'] and 'perf_data' in o:
        o['performance_data'] = o['perf_data']

    # If this is a service (as opposed to host) lets add service_description field in out putput
    if 'service_description' in o:
        template += "service_description={service_description}\n"
    if not o['performance_data'].endswith('\\n'):
        o['performance_data'] += '\\n'
    # Format the string and return
    return template.format(**o) + '\n'


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


_host_check_result = """
host_name={host_name}
check_type={check_type}
check_options=0
scheduled_check=1
reschedule_check=1
latency=0.0
start_time={start_time}
finish_time={finish_time}
early_timeout=0
exited_ok=1
return_code={return_code}
output={plugin_output}{long_plugin_output} | {performance_data}
"""
