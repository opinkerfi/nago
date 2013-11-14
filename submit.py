#!/usr/bin/env python

import nago
host_result = {}
host_result['host_name'] = "localhost"
host_result['return_code'] = "3"
host_result['plugin_output'] = 'test output'
host_result['performance_data'] = 'perfdata=1'

print nago.post_checkresults(hosts=[host_result])
