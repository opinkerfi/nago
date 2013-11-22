# -*- coding: utf-8 -*-

""" Get and post nagios checkresults between nago instances

This extension allows to get status data from a local nagios server.

Also pushing checkresults into a local nagios server, therefore updating nagios status.
"""
from pynag.Parsers import mk_livestatus, config
import time
import os
import os.path
import tempfile
from nago.core import nago_access


@nago_access
def get():
    """ Get all nagios status information from a local nagios instance
    """
    livestatus = mk_livestatus()
    hosts = livestatus.get_hosts()
    services = livestatus.get_services()
    result = {}
    result['hosts'] = hosts
    result['services'] = services
    return result

@nago_access
def post(hosts=None, services=None, check_existance=True, create_services=True, create_hosts=False):
    """ Puts a list of hosts into local instance of nagios checkresults
    Arguments:
      hosts               -- list of dicts, like one obtained from get_checkresults
      services            -- list of dicts, like one obtained from get_checkresults
      check_existance     -- If True, check (and log) if objects already exist before posting
      create_services -- If True, autocreate non-existing services (where the host already exists)
      create_hosts    -- If True, autocreate non-existing hosts
    """

    nagios_config = config()
    nagios_config.parse_maincfg()
    check_result_path = c.get_cfg_value("check_result_path")


    fd, filename = tempfile.mkstemp(prefix='c', dir=check_result_path)
    if not hosts:
        hosts = []
    if not services:
        services = []

    if check_existance:
        checkresults_overhaul(hosts, services, create_services=create_services, create_hosts=create_hosts)
    checkresults = '### Active Check Result File Made by Nago ###\n'
    checkresults += 'file_time=%s' % (int(time.time()))
    checkresults = ''

    for host in hosts:
        checkresults += _format_checkresult(**host)
    for service in services:
        checkresults += _format_checkresult(**service)
    os.write(fd, checkresults)

    # Cleanup and make sure our file is readable by nagios
    os.close(fd)
    os.chmod(filename, 0644)

    # Create an ok file, so nagios knows it's ok to reap our changes
    file('%s.ok' % filename, 'w')


def checkresults_overhaul(hosts, services, create_services, create_hosts):
    """ Iterates through hosts and services, and filters out those who do not exist in our local monitoring core

    If create_services or create_hosts are defined, then
    """


def _format_checkresult(**kwargs):
    """ Returns a string in a nagios "checkresults" compatible format """
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


# This is an example of what checkresult file looks like to nagios. This is used by
# _format_checkresult()
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
