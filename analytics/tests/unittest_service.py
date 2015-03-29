#!/usr/bin/env python

# import libs
import unittest
import json
import sys
import os
from types import DictType
# import classes
import analytics.utils.misc as misc
import analytics.exceptions.exceptions as ex
import analytics.service as service
import projectpaths as paths
from analytics.loading.jsonloader import JsonLoader
from analytics.loading.xmlloader import XmlLoader


general_input = [
    None, True, False, sys.maxint, -sys.maxint-1, {}, [],
    {"1": 1, "2": 2}, [1, 2, 3, 4, 5], "abc", 0, 1, -1, 1.233,
    -3.343, 0.23435, " string ", " test test test ", "1"
]

class Service_TestSequence(unittest.TestCase):
    def test_service_isUserInEmaillist(self):
        for item in general_input:
            self.assertEqual(service.isUserInEmaillist(item), False)
        for item in service.EMAIL_LIST:
            self.assertEqual(service.isUserInEmaillist(item), True)

    def test_service_searchDatasets(self):
        scanls = []
        for root, dirs, files in os.walk(paths.DATASETS_PATH):
            for file in files:
                if file == "manifest.json":
                    scanls.append(os.path.join(root, file))
        ls = service.searchDatasets()
        self.assertEqual(len(ls), len(scanls))

    def test_service_loaderForDatatype(self):
        for item in general_input:
            with self.assertRaises(ex.AnalyticsStandardError):
                service._loaderForDatatype(item, item)
        # test json loader
        loader = service._loaderForDatatype("json", "path")
        self.assertEqual(type(loader), JsonLoader)
        self.assertEqual(loader._filepath, "path")
        # test xml loader
        loader = service._loaderForDatatype("xml", "path")
        self.assertEqual(type(loader), XmlLoader)
        self.assertEqual(loader._filepath, "path")

    def test_service_generateErrorMessage(self):
        messages = ["test"]
        code = 401
        obj = service._generateErrorMessage(messages, code)
        self.assertEqual(type(obj), DictType)
        self.assertEqual(obj["messages"], messages)
        self.assertEqual(obj["code"], code)
        self.assertEqual(obj["status"], "error")

    def test_service_generateSuccessMessage(self):
        messages = ["test"]
        dataobj = {"test": "test"}
        obj = service._generateSuccessMessage(messages, dataobj)
        self.assertEqual(type(obj), DictType)
        self.assertEqual(obj["messages"], messages)
        self.assertEqual(obj["data"], dataobj)
        self.assertEqual(obj["status"], "success")


# Load test suites
def _suites():
    return [
		Service_TestSequence
    ]

# Load tests
def loadSuites():
    # global test suite for this module
    gsuite = unittest.TestSuite()
    for suite in _suites():
        gsuite.addTest(unittest.TestLoader().loadTestsFromTestCase(suite))
    return gsuite

if __name__ == '__main__':
    suite = loadSuites()
    print ""
    print "### Running tests ###"
    print "-" * 70
    unittest.TextTestRunner(verbosity=2).run(suite)
