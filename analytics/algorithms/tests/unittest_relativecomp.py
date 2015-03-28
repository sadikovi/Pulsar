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
import warnings
import random
# import classes
import analytics.exceptions.exceptions as ex
import analytics.algorithms.relativecomp as rc
import analytics.algorithms.rank as rank
import analytics.core.processor.processor as processor
from analytics.core.map.elementmap import ElementMap
from analytics.core.map.pulsemap import PulseMap


class RelComp_TestSequence(unittest.TestCase):
    def setUp(self):
        self.isStarted = True

    def test_relcomp_init(self):
        with self.assertRaises(ex.AnalyticsStandardError):
            a = rc._RelComp()

    def test_relcomp_alpha(self):
        self.assertEqual(rc._RelComp.alpha(), 1)

    def test_relcomp_beta(self):
        alpha = rc._RelComp.alpha()
        delta = 0.8
        with self.assertRaises(ex.AnalyticsStandardError):
            k = -1
            rc._RelComp.beta(alpha, k, delta)
        with self.assertRaises(ex.AnalyticsStandardError):
            k = 1.1
            rc._RelComp.beta(alpha, k, delta)
        k = 1
        self.assertEqual(rc._RelComp.beta(alpha, k, delta), 0)
        k = 0
        self.assertTrue(1 >= rc._RelComp.beta(alpha, k, delta) >= 0 )
        for _i in range(10):
            k = random.random();
            delta = random.randrange(1, 10)*random.random()
            self.assertTrue(1 >= rc._RelComp.beta(alpha, k, delta) >= 0)

    def test_relcomp_k(self):
        for i in range(10):
            p = random.randrange(1, 1000)
            r = p * random.random()
            rmedian = p * random.random()
            da = random.randrange(1, 100)*random.random()
            self.assertTrue(1 >= rc._RelComp.k(r, rmedian, da) >= 0)

    def test_relcomp_dr(self):
        for _i in range(10):
            p = random.randrange(1, 1000)
            r = p * random.random()
            rmedian = p * random.random()
            i = random.randrange(1, 100)
            m = random.randrange(1, 100)
            self.assertTrue(rc._RelComp.dr(r, rmedian, i, m) >= 0)

    def test_relcomp_da(self):
        a = []
        with self.assertRaises(ex.AnalyticsStandardError):
            rc._RelComp.da(a)
        # 28.03.2015: ivan sadikov - changed test according to modification
        #   [array len == 1]
        a = [random.randrange(0, 100)]
        self.assertEqual(rc._RelComp.da(a), 1.0)
        for _i in range(10):
            a = [random.randrange(0, 100) for i in range(10)]
            a = sorted(a)
            self.assertTrue(rc._RelComp.da(a) > 0)


class RelativeComparison_TestSequence(unittest.TestCase):
    def setUp(self):
        self.isStarted = True
        self._rel = rc.RelativeComparison()
        self._a = [
                {"name": "value", "desc": "value", "sample": 123, "dynamic": True, "priority": -1},
                {"name": "price", "desc": "price", "sample": 320.0, "dynamic": False, "priority": 1},
                {"name": "amount", "desc": "amount", "sample": 3, "dynamic": True}
        ]
        self._b = [
            {"id": "1","name": "#1","desc": "", "cluster": "A", "value": 100, "price": 320.0, "amount": 1},
            {"id": "2","name": "#2","desc": "", "cluster": "A", "value": 120, "price": 300.0, "amount": 4},
            {"id": "3","name": "#3","desc": "", "cluster": "A", "value": 140, "price": 199.0, "amount": 3},
            {"id": "4","name": "#4","desc": "", "cluster": "A", "value": 124, "price": 234.0, "amount": 5},
            {"id": "5","name": "#5","desc": "", "cluster": "A", "value": 150, "price": 250.0, "amount": 9},
            {"id": "6","name": "#6","desc": "", "cluster": "A", "value": 128, "price": 245.0, "amount": 3},
            {"id": "7","name": "#7","desc": "", "cluster": "A", "value": 125, "price": 230.0, "amount": 2}
        ]

    def test_relativecomp_init(self, setUp=None):
        rel = rc.RelativeComparison()
        self.assertEqual(rel._id, rc.ID)
        self.assertEqual(rel._name, rc.LONG_NAME)
        self.assertEqual(rel._short, rc.SHORT_NAME)

    def test_relativecomp_hashkeyForList(self):
        list = []
        self.assertEqual(self._rel._hashkeyForList(list), "")
        list = range(0, random.randrange(1, 20))
        random.shuffle(list)
        self.assertTrue(len(self._rel._hashkeyForList(list)) > 0)

    def test_relativecomp_threadHash(self):
        ti = 1; sti = 1
        self.assertEqual(self._rel._threadHash("", ""), "#")
        self.assertEqual(self._rel._threadHash(ti, sti), str(ti)+"#"+str(sti))

    def test_relativecomp_relcomp(self):
        self.assertEqual(self._rel._relcomp([], 1, 1), {})
        with self.assertRaises(ex.AnalyticsCheckError):
            median = random.randrange(1000, 2000)
            order = (-1)**random.randrange(0, 2)
            self._rel._relcomp(None, order, median)
        with self.assertRaises(ex.AnalyticsStandardError):
            median = random.randrange(1000, 2000)
            order = (-1)**random.randrange(0, 2)
            self._rel._relcomp([1, 2, 3], order, median)
        for i in range(10):
            a = [random.randrange(0, 100)*((-1)**random.randrange(0, 2)) for i in range(10)]
            order = (-1)**random.randrange(0, 2)
            median_index = random.randrange(0, len(a))
            median = a[median_index]
            res = self._rel._relcomp(a, order, median)
            self.assertEqual(len(res.keys()), len(set(a)))
            self.assertEqual(res[median], 1)
            for key in res.keys():
                self.assertTrue(key in a)
                self.assertTrue(1 >= res[key] >= 0)

    def test_relativecomp_frontier(self):
        map = {}
        self.assertEqual(self._rel._frontier(map), {})

        map = {}
        for _i in range(20):
            aa = [random.randrange(2, 10) for _j in range(3)]
            map[self._rel._hashkeyForList(aa)] = aa
        self.assertEqual(self._rel._frontier(map), {})

        for _k in range(10):
            map = {}
            for _i in range(20):
                aa = [random.random() for _j in range(3)]
                map[self._rel._hashkeyForList(aa)] = aa
            hashRank = self._rel._frontier(map)
            self.assertEqual(len(hashRank.keys()), len(map.keys()))
            for key in hashRank.keys():
                self.assertEqual(type(hashRank[key]), rank.Rank)
                self.assertTrue(hashRank[key] is not rank.RSYS.UND_RANK)

    def test_relativecomp_computeRank(self):
        with self.assertRaises(ex.AnalyticsCheckError):
            self._rel._computeRanks([], [], [])
        with self.assertRaises(ex.AnalyticsCheckError):
            self._rel._computeRanks({}, {}, [])
        for _kl in range(10):
            n = random.randrange(1, 3)
            orders = [(-1)**random.randrange(0, 2) for _i in range(n)]
            medians = []; a = {}
            for _i in range(20):
                aa = [random.randrange(0, 100)*random.random() for _j in range(n)]
                a[self._rel._hashkeyForList(aa)] = aa
                if _i == 5: medians = aa
            hashRank = self._rel._computeRanks(a, orders, medians)
            self.assertEqual(len(hashRank.keys()), len(a.keys()))
            for key in hashRank.keys():
                self.assertEqual(type(hashRank[key]), rank.Rank)
                self.assertNotEqual(hashRank[key], rank.RSYS.UND_RANK)

    def test_relativecomp_rankResults_err(self):
        with self.assertRaises(ex.AnalyticsCheckError):
            self._rel.rankResults({}, {})

    def test_relativecomp_rankResults(self):
        # initialise maps and idmapper
        pulses = PulseMap(); elements = ElementMap(); idmapper = {}
        idmapper = processor.parseElements(self._b, elements, idmapper)
        idmapper = processor.parsePulses(self._a, pulses, idmapper)
        # rank elements
        res = self._rel.rankResults(elements, pulses)
        self.assertEqual(len(elements._map.values()), len(self._b))
        for element in elements._map.values():
            self.assertNotEqual(element.rank()._name, rank.RSYS.UND_RANK._name)

    def test_relativecomp_rankResults_warn(self):
        # initialise maps and idmapper
        pulses = PulseMap(); elements = ElementMap(); idmapper = {}
        idmapper = processor.parseElements(self._b, elements, idmapper)
        idmapper = processor.parsePulses(self._a, pulses, idmapper)
        # make all pulses dynamic
        for pulse in pulses._map.values():
            pulse.setStatic(False)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # rank elements
            res = self._rel.rankResults(elements, pulses)
            self.assertEqual(len(elements._map.values()), len(self._b))
            for element in elements._map.values():
                self.assertNotEqual(element.rank()._name, rank.RSYS.UND_RANK._name)
            # warnings assertion
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, UserWarning))


# Load test suites
def _suites():
    return [
        RelComp_TestSequence,
        RelativeComparison_TestSequence
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
