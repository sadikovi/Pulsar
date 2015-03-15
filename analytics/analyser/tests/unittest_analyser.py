#!/usr/bin/env python

# import libs
import unittest
from types import ListType
import warnings
# import classes
import analytics.exceptions.exceptions as ex
import analytics.algorithms.algorithmsmap as a
import analytics.algorithms.algorithm as al
import analytics.algorithms.relativecomp as rc
import analytics.datavalidation.propertiesmap as prmap
import analytics.datavalidation.resultsmap as rsmap
import analytics.analyser.analyser as anl


class Analyser_TestsSequence(unittest.TestCase):
    def setUp(self):
        self.isStarted = True
        self._analyser = anl.Analyser()

    def test_analyser_init(self, setUp = None):
        a = anl.Analyser()
        self.assertNotEqual(a._algorithmsmap, None)
        self.assertEqual(len(a._algorithmsmap.keys()), 1)
        self.assertNotEqual(a._defaultAlgorithm, None)
        self.assertEqual(a._defaultAlgorithm, a._algorithmsmap.values()[0])

    def test_analyser_setDefaultAlgorithm(self):
        with self.assertRaises(ex.AnalyticsTypeError):
            self._analyser._setDefaultAlgorithm(None)
        with self.assertRaises(ex.AnalyticsTypeError):
            self._analyser._setDefaultAlgorithm({})
        t = rc.RelativeComparison()
        self._analyser._setDefaultAlgorithm(t)
        self.assertEqual(self._analyser._defaultAlgorithm, t)

    def test_analyser_hasAlgorithmsMap(self):
        self.assertEqual(self._analyser._hasAlgorithmsMap(), True)

    def test_analyser_allAlgorithms(self):
        t = self._analyser.allAlgorithms()
        self.assertEqual(type(t), ListType)
        self.assertEqual(len(t), 1)
        self.assertEqual(t[0]._id, rc.RelativeComparison()._id)

    def test_analyser_getAlgorithm(self):
        self.assertEqual(self._analyser.getAlgorithm(None), None)
        self.assertEqual(self._analyser.getAlgorithm("$"), None)
        t = rc.RelativeComparison()
        self.assertEqual(self._analyser.allAlgorithms()[0]._id, t._id)

    def test_analyser_analyseUsingAlgorithm(self):
        t = rc.RelativeComparison()
        rmap = rsmap.ResultsMap()
        pmap = prmap.PropertiesMap()
        with self.assertRaises(ex.AnalyticsTypeError):
            self._analyser.analyseUsingAlgorithm(None, [], [])
        with self.assertRaises(ex.AnalyticsCheckError):
            self._analyser.analyseUsingAlgorithm(t, [], [])
        with self.assertRaises(ex.AnalyticsCheckError):
            self._analyser.analyseUsingAlgorithm(t, rmap, {})
        res = self._analyser.analyseUsingAlgorithm(t, rmap, pmap)
        self.assertEqual(res, rmap)

    def test_analyser_analyseUsingMap(self):
        t = rc.RelativeComparison()
        rmap = rsmap.ResultsMap()
        pmap = prmap.PropertiesMap()
        with self.assertRaises(ex.AnalyticsCheckError):
            self._analyser.analyseUsingMap(None, rmap, prmap)
        with self.assertRaises(ex.AnalyticsStandardError):
            self._analyser.analyseUsingMap(a.AlgorithmsMap(), rmap, pmap, False)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            self._analyser.analyseUsingMap(a.AlgorithmsMap(), rmap, pmap, True)
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[-1].category, UserWarning))
            self.assertEqual("No algorithm is specified, default algorithm will be used", str(w[-1].message))
        self._analyser.analyseUsingMap(self._analyser._algorithmsmap, rmap, pmap)


# Load test suites
def _suites():
    return [
        Analyser_TestsSequence
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
