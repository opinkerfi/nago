#!/usr/bin/env python
__author__ = 'palli'
import unittest
import nago.extensions
import time


class TestExtensions(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCheckResults(self):
        r = nago.extensions.checkresults.get()
        nago.extensions.checkresults.post(**r)
