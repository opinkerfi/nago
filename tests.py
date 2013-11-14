#!/usr/bin/env python
__author__ = 'palli'
import unittest
import nago
import time


class testNago(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def testPostCheckResults(self):
        host_name = "localhost"
        service_description = "nago service check"
        start_time = '%.5f' % time.time()
        finish_time = '%.5f' % time.time()
        return_code = 0
        plugin_output = "test service"
        long_plugin_output = ""
        check_type=0
        performance_data = "perfdata=1"
        services = [locals()]
        hosts = [locals()]

        r = nago.get_checkresults()
        nago.post_checkresults(**r)
