#!/usr/bin/env python

# import libs
import unittest
import sys
import os
import random
import uuid
# import classes
import analytics.utils.misc as misc
import analytics.exceptions.exceptions as ex
import analytics.service as service
from analytics.datamanager.datamanager import DataManager


class IntegrationTestSequence(unittest.TestCase):
    def setUp(self):
        filepath = os.path.dirname(os.path.realpath(__file__))
        self.integrationpath = os.path.join(filepath, "datasets")
        self.datamanager = DataManager()
        self.datamanager.loadDatasets(self.integrationpath)
        self.datasets = self.datamanager._datasets

    def test_service_default(self):
        query = ""
        datasetId = random.choice(self.datasets.keys())
        result = service.requestData(datasetId, query, self.datamanager)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["code"], 200)

    def test_service_wrongquery(self):
        query = uuid.uuid4().hex
        datasetId = random.choice(self.datasets.keys())
        result = service.requestData(datasetId, query, self.datamanager)
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["code"], 400)

    def test_service_simpleQuery(self):
        query = """select from ${pulses}
                    where @1b4cf15c86ec31cd8838feab0f9856b1 |is| static
                        and @1b4cf15c86ec31cd8838feab0f9856b1 = 2
                        and @b6db26b3972932b2862dac41cbb1493d = [up]"""
        datasetId = random.choice(self.datasets.keys())
        result = service.requestData(datasetId, query, self.datamanager)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["code"], 200)

    def test_service_selectCluster(self):
        query = """select from ${clusters}
                    where @id = [bc27b4dbbc0f34f9ae8e4b72f2d51b60]"""
        datasetId = random.choice(self.datasets.keys())
        result = service.requestData(datasetId, query, self.datamanager)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["code"], 200)

    def service_warnings(self, warn=True):
        query = """select from ${pulses}
                    where @f4b9ea9d3bf239f5a1c80578b0556a5e |is| dynamic"""
        datasetId = random.choice(self.datasets.keys())
        result = service.requestData(
            datasetId,
            query,
            self.datamanager,
            iswarnings=warn
        )
        # result should not fail and should generate warnings
        return result

    def test_service_warnings_on(self):
        # warnings are on by default
        result = self.service_warnings()
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["code"], 200)
        self.assertEqual(len(result["messages"]), 1)

    def test_service_warnings_off(self):
        # warning is expected, but we turn it off
        result = self.service_warnings(False)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["code"], 200)
        self.assertEqual(len(result["messages"]), 0)


# Load test suites
def _suites():
    return [
		IntegrationTestSequence
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
