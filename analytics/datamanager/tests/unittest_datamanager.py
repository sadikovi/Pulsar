#!/usr/bin/env python

# import libs
import unittest
import os
# import classes
import analytics.exceptions.exceptions as ex
import analytics.datamanager.datamanager as dm


class DataManager_TestsSequence(unittest.TestCase):
    def setUp(self):
        self.isStarted = True

    def test_datamanager_init(self):
        t = dm.DataManager()
        self.assertEqual(t._directory, dm._DIRECTORY)
        self.assertEqual(t._manifests, [])
        self.assertEqual(t._datasets, {})

    def test_datamanager_reset(self):
        t = dm.DataManager()
        self.assertEqual(t._directory, dm._DIRECTORY)
        self.assertEqual(t._manifests, [])
        self.assertEqual(t._datasets, {})
        t.setSearchPath("test")
        t._manifests.append(1)
        t._datasets["1"] = 1
        self.assertEqual(t._directory, "test")
        self.assertEqual(t._manifests, [1])
        self.assertEqual(t._datasets, {"1":1})
        t.resetToDefault()
        self.assertEqual(t._directory, dm._DIRECTORY)
        self.assertEqual(t._manifests, [])
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
        self.assertEqual(dataset._groups, { "path": os.path.join(directory, "test", "groups.json"), "type": "json" })
        self.assertEqual(dataset._results, { "path": os.path.join(directory, "test", "results.json"), "type": "json" })
        self.assertEqual(dataset._properties, { "path": os.path.join(directory, "test", "properties.json"), "type": "json" })

    def test_datamanager_findManifests(self):
        t = dm.DataManager()
        with self.assertRaises(ex.AnalyticsCheckError):
            t._findManifests({})
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datasets")
        t.setSearchPath(directory)
        t._findManifests(t._directory)
        self.assertEqual(len(t._manifests), 2)
        self.assertEqual(t._manifests[0], os.path.join(directory, "test", "manifest.json"))

    def test_datamanager_loadDatasets(self):
        directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datasets")
        t = dm.DataManager()
        t.setSearchPath(directory)
        t.loadDatasets()
        self.assertEqual(len(t._manifests), 2)
        self.assertEqual(len(t._datasets.values()), 1)


# Load test suites
def _suites():
    return [
        DataManager_TestsSequence
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
