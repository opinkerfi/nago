#!/usr/bin/env python
__author__ = 'palli'
import unittest
import nago.extensions
import time
import tempfile
import platform


class TestExtensions(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCheckResults(self):
        r = nago.extensions.checkresults.get()
        nago.extensions.checkresults.post(**r)


import nago.settings

class TestSettings(unittest.TestCase):
    def setUp(self):
        defaults = {}
        defaults['main'] = {}
        defaults['main']['test_option'] = 'default value'

        self.original_defaults = nago.settings.defaults
        self.original_cfg_file = nago.settings.cfg_file

        self.defaults = defaults
        self.cfg_file = tempfile.mktemp(prefix='nago', suffix='.ini')
        nago.settings.cfg_file = tempfile.mktemp(prefix='nago', suffix='.ini')

    def tearDown(self):
        nago.settings.cfg_file = self.original_cfg_file
        nago.settings.defaults = self.original_defaults

    def testGetOptions(self):
        """ Test the defaults """
        host_name = nago.settings.get_option('host_name')
        default_hostname = platform.node()
        self.assertEqual(default_hostname, host_name)

        default_hostname = 'default'
        host_name = nago.settings.get_option('host_name', default=default_hostname)
        self.assertEqual(default_hostname, host_name)

    def testSetOptions(self):
        option_name = 'test_option'
        section_name = 'new section'
        new_value = 'new value'
        kwargs = {option_name:new_value}

        nago.settings.set_option(section=section_name, cfg_file=self.cfg_file, **kwargs)

        result = nago.settings.get_option(option_name=option_name, section_name=section_name, cfg_file=self.cfg_file)
        self.assertEqual(new_value, result)

    def testGenerateConfig(self):
        import nago.settings
        default_value = self.defaults['main']['test_option']
        nago.settings.generate_configfile(cfg_file=self.cfg_file, defaults=self.defaults)
        actual_value = nago.settings.get_option('test_option', cfg_file=self.cfg_file)
        self.assertEqual(default_value, actual_value)
