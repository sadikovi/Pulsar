#!/usr/bin/env python

'''
Copyright 2015 Ivan Sadikov

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''


# import libs
import unittest
import os
from types import DictType
# import classes
import projectpaths as paths
import analytics.exceptions.exceptions as ex
import analytics.datamanager.datamanager as dm


class DataManager_TestSequence(unittest.TestCase):
    def setUp(self):
        self.isStarted = True

    def test_datamanager_init(self):
        t = dm.DataManager()
        self.assertEqual(t._directory, dm._DIRECTORY)
        self.assertEqual(t._manifests, {})
        self.assertEqual(t._datasets, {})

    def test_datamanager_reset(self):
        t = dm.DataManager()
        self.assertEqual(t._directory, dm._DIRECTORY)
        self.assertEqual(t._manifests, {})
        self.assertEqual(t._datasets, {})
        t.setSearchPath("test")
        t._manifests["root"] = "root/manifest.json"
        t._datasets["1"] = 1
        self.assertEqual(t._directory, "test")
        self.assertEqual(t._manifests, {"root":"root/manifest.json"})
        self.assertEqual(t._datasets, {"1":1})
        t.resetToDefault()
        self.assertEqual(t._directory, dm._DIRECTORY)
        self.assertEqual(t._manifests, {})
        self.assertEqual(t._datasets, {})

    def test_datamanager_parseManifest(self):
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datasets")
        right_dir = os.path.join(directory, "test", "manifest.json")
        wrong_dir = os.path.join("wrong_dir", "manifest.json")
        wrong_manifest = os.path.join(directory, "wrongtest", "manifest.json")
        t = dm.DataManager()
        self.assertEqual(t._parseManifest(wrong_dir), False)
        self.assertEqual(t._parseManifest(wrong_manifest), False)
        self.assertEqual(t._parseManifest(right_dir), True)
        self.assertEqual(len(t._datasets.values()), 1)
        dataset = t._datasets.values()[0]
        self.assertEqual(dataset._id, "test")
        self.assertEqual(dataset._name, "Test dataset")
        self.assertEqual(dataset._desc, "Test dataset")
        self.assertEqual(dataset._discover, False)
        self.assertEqual(dataset._clusters,
            {
                "path": os.path.join(directory, "test", "clusters.json"),
                "type": "json"
            }
        )
        self.assertEqual(dataset._elements,
            {
                "path": os.path.join(directory,
                "test", "elements.json"), "type": "json"
            }
        )
        self.assertEqual(dataset._pulses,
            {
                "path": os.path.join(directory, "test", "pulses.json"),
                "type": "json"
            }
        )

    def test_datamanager_findManifests(self):
        t = dm.DataManager()
        with self.assertRaises(ex.AnalyticsCheckError):
            t._findManifests({})
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datasets")
        t.setSearchPath(directory)
        t._findManifests(t._directory)
        self.assertEqual(len(t._manifests.keys()), 2)
        tempdir = os.path.join(directory, "test")
        self.assertEqual(t._manifests[tempdir], os.path.join(tempdir, "manifest.json"))

    def test_datamanager_loadDatasets(self):
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datasets")
        t = dm.DataManager()
        t.setSearchPath(directory)
        t.loadDatasets()
        self.assertEqual(len(t._manifests.keys()), 2)
        self.assertEqual(len(t._datasets.values()), 1)

    def test_datamanager_testDatasets(self):
        directory = os.path.join(paths.ANALYTICS_PATH, "datasets")
        t = dm.DataManager()
        res = t.util_testDatasets(directory)
        # select manifest and dataset results
        manfs = res["manifests"]
        ds = res["datasets"]
        self.assertEqual(type(manfs), DictType)
        self.assertEqual(type(ds), DictType)
        self.assertEqual(len(manfs.keys()), len(ds.keys()))
        # check manifests
        for manf in manfs.values():
            self.assertEqual(manf["manifest"], True)
            self.assertEqual(manf["dataset"], True)
        # check datasets
        for dsf in ds.values():
            self.assertEqual(dsf["clusters"], True)
            self.assertEqual(dsf["elements"], True)
            if "pulses" in dsf:
                self.assertEqual(dsf["pulses"], True)

    def test_datamanager_checkDatasetTest(self):
        directory = os.path.join(paths.ANALYTICS_PATH, "datasets")
        t = dm.DataManager()
        res = t.util_testDatasets(directory)
        self.assertEqual(t.util_checkDatasetsResult(res), True)


# Load test suites
def _suites():
    return [
        DataManager_TestSequence
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
