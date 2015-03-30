#!/usr/bin/env python

# import libs
import unittest
from types import IntType, FloatType, ListType
import random
import warnings
# import classes
import analytics.exceptions.exceptions as ex
import analytics.core.processor.processor as processor
import analytics.selector.selector as selector
from analytics.core.map.clustermap import ClusterMap
from analytics.core.map.elementmap import ElementMap
from analytics.core.map.pulsemap import PulseMap
from analytics.algorithms.algorithmsmap import AlgorithmsMap
from analytics.algorithms.algorithm import Algorithm


class Selector_TestSequence(unittest.TestCase):
    def setUp(self):
        self._p = [
            {"id": "1", "name": "random", "desc": "random", "sample": 1, "dynamic": True},
            {"id": "2", "name": "order", "desc": "order", "sample": 1.0, "dynamic": False},
            {"id": "3", "name": "dir", "desc": "dir", "sample": "str"}
        ]
        self._c = [
            {"id": "1", "name": "#1", "desc": "#1", "parent": None},
            {"id": "2", "name": "#2", "desc": "#2", "parent": "1"},
            {"id": "3", "name": "#3", "desc": "#3", "parent": "1"},
            {"id": "4", "name": "#4", "desc": "#4", "parent": "2"},
            {"id": "5", "name": "#5", "desc": "#5", "parent": "2"}
        ]
        self._e = [
            {"id": "1", "name": "@1", "desc": "@1", "cluster": "5", "random": 2, "order": 1.2, "dir": "up"},
            {"id": "2", "name": "@2", "desc": "@2", "cluster": "5", "random": 9, "order": 0.9, "dir": "down"},
            {"id": "3", "name": "@3", "desc": "@3", "cluster": "3", "random": 7, "order": 1.1, "dir": "down"},
            {"id": "4", "name": "@4", "desc": "@4", "cluster": "3", "random": 1, "order": 1.5, "dir": "up"},
            {"id": "5", "name": "@5", "desc": "@5", "cluster": "4", "random": 4, "order": 1.7, "dir": "down"}
        ]
        # create process block
        block = processor.ProcessBlock(
            {"map": ClusterMap(), "data": self._c},
            {"map": ElementMap(), "data": self._e},
            {"map": PulseMap(), "data": self._p}
        )
        # parse object lists
        block = processor.processWithBlock(block)
        self._clustermap = block._clustermap
        self._elementmap = block._elementmap
        self._pulsemap = block._pulsemap
        # create algorithms map
        self._algorithmsmap = AlgorithmsMap()
        self._algorithmsmap.assign(Algorithm("%1", "%1", "%1"))

    def query_empty(self):
        return ""

    def query_cluster_select(self, cid):
        return "select from ${clusters} where @id=[%s]" %(cid)

    def query_pulse_static_select(self, pid, value):
        value = value if type(value) in [IntType, FloatType] else "[%s]"%(value)
        return "select from ${pulses} where @%s=%s and @%s |is| static"%(pid, str(value), pid)

    def query_pulse_dynamic_select(self, pid, value):
        value = value if type(value) in [IntType, FloatType] else "[%s]"%(value)
        return "select from ${pulses} where @%s=%s and @%s |is| dynamic"%(pid, str(value), pid)

    def query_all_select_static(self, cid, pid, value):
        value = value if type(value) in [IntType, FloatType] else "[%s]"%(value)
        return ";".join([
            "select from ${clusters} where @id=[%s]" %(cid),
            "select from ${pulses} where @%s=%s and @%s |is| static"%(pid, str(value), pid)
        ])

    def query_all_select_dynamic(self, cid, pid, value):
        value = value if type(value) in [IntType, FloatType] else "[%s]"%(value)
        return ";".join([
            "select from ${clusters} where @id=[%s]" %(cid),
            "select from ${pulses} where @%s=%s and @%s |is| dynamic"%(pid, str(value), pid)
        ])

    def test_selector_valid_query(self):
        queries = [
            self.query_empty(),
            self.query_cluster_select("1"),
            self.query_pulse_static_select("2", 1),
            self.query_pulse_dynamic_select("3", 1),
            self.query_all_select_static("4", "5", 1),
            self.query_all_select_dynamic("4", "5", 1)
        ]
        for query in queries:
            a = selector.parseQueryset(query)
            self.assertEqual(type(a), ListType)

    def test_selector_integration_test1(self):
        # create filter block
        block = selector.FilterBlock(
            self._algorithmsmap,
            self._pulsemap,
            self._clustermap,
            self._elementmap
        )
        # filter with selector
        block = selector.filterWithBlock(
            self.query_empty(),
            block
        )
        # reassign maps to new values
        self._algorithmsmap = block._alg
        self._pulsemap = block._pul
        self._clustermap = block._clu
        self._elementmap = block._ele
        # assertion
        self.assertEqual(len(self._algorithmsmap._map.values()), 1)
        self.assertEqual(len(self._pulsemap._map), len(self._p))
        self.assertEqual(len(self._clustermap._map), len(self._c))
        self.assertEqual(len(self._elementmap._map), len(self._e))

    def test_selector_integration_test1(self):
        # create filter block
        block = selector.FilterBlock(
            self._algorithmsmap,
            self._pulsemap,
            self._clustermap,
            self._elementmap
        )
        # extract parameters: cluster id
        cluster_values = self._clustermap._map.values()
        cid = [x.id() for x in cluster_values if x.name() == "#2"][0]
        block = selector.filterWithBlock(self.query_cluster_select(cid), block)
        # reassign maps to new values
        self._algorithmsmap = block._alg
        self._pulsemap = block._pul
        self._clustermap = block._clu
        self._elementmap = block._ele
        # assertion
        self.assertEqual(len(self._algorithmsmap._map.values()), 1)
        self.assertEqual(len(self._pulsemap._map), 3)
        self.assertEqual(len(self._clustermap._map), 3)
        self.assertEqual(len(self._elementmap._map), 3)

    def test_selector_integration_test2(self):
        # create filter block
        block = selector.FilterBlock(
            self._algorithmsmap,
            self._pulsemap,
            self._clustermap,
            self._elementmap
        )
        # extract parameters: pulse id and default value
        pulse_values = self._pulsemap._map.values()
        pid = [x.id() for x in pulse_values if x.name() == "random"][0]
        value = 2
        block = selector.filterWithBlock(
            self.query_pulse_static_select(pid, value),
            block
        )
        # reassign to maps
        self._algorithmsmap = block._alg
        self._pulsemap = block._pul
        self._clustermap = block._clu
        self._elementmap = block._ele
        # assertion
        self.assertEqual(len(self._algorithmsmap._map.values()), 1)
        self.assertEqual(len(self._pulsemap._map), 3)
        self.assertEqual(self._pulsemap.get(pid).static(), True)
        self.assertEqual(self._pulsemap.get(pid).default(), value)
        self.assertEqual(len(self._clustermap._map), 5)
        self.assertEqual(len(self._elementmap._map), 1)
        self.assertEqual(self._elementmap._map.values()[0].name(), "@1")

    def test_selector_integration_test3(self):
        # filter block
        block = selector.FilterBlock(
            self._algorithmsmap,
            self._pulsemap,
            self._clustermap,
            self._elementmap
        )
        pulse_values = self._pulsemap._map.values()
        pid = [x.id() for x in pulse_values if x.name() == "order"][0]
        value = 20.0
        block = selector.filterWithBlock(
            self.query_pulse_dynamic_select(pid, value),
            block
        )
        # reassign to maps
        self._algorithmsmap = block._alg
        self._pulsemap = block._pul
        self._clustermap = block._clu
        self._elementmap = block._ele
        # assertion
        self.assertEqual(len(self._algorithmsmap._map.values()), 1)
        self.assertEqual(len(self._pulsemap._map), 3)
        self.assertEqual(self._pulsemap.get(pid).static(), False)
        self.assertEqual(self._pulsemap.get(pid).default(), value)
        self.assertEqual(len(self._clustermap._map), 5)
        self.assertEqual(len(self._elementmap._map), 5)

    def test_selector_integration_test4(self):
        # filter block
        block = selector.FilterBlock(
            self._algorithmsmap,
            self._pulsemap,
            self._clustermap,
            self._elementmap
        )
        # extract parameters: cluster id, pulse id and default value
        cluster_values = self._clustermap._map.values()
        cid = [x.id() for x in cluster_values if x.name() == "#3"][0]
        pulse_values = self._pulsemap._map.values()
        pid = [x.id() for x in pulse_values if x.name() == "random"][0]
        value = 7
        block = selector.filterWithBlock(
            self.query_all_select_static(cid, pid, value),
            block
        )
        # reassign parameters to maps
        self._algorithmsmap = block._alg
        self._pulsemap = block._pul
        self._clustermap = block._clu
        self._elementmap = block._ele
        # assertion
        self.assertEqual(len(self._algorithmsmap._map.values()), 1)
        self.assertEqual(len(self._pulsemap._map), 3)
        self.assertEqual(self._pulsemap.get(pid).static(), True)
        self.assertEqual(self._pulsemap.get(pid).default(), value)
        self.assertEqual(len(self._clustermap._map), 1)
        self.assertEqual(len(self._elementmap._map), 1)

    def test_selector_integration_test5(self):
        # filter block
        block = selector.FilterBlock(
            self._algorithmsmap,
            self._pulsemap,
            self._clustermap,
            self._elementmap
        )
        # extract parameters: cluster id, pulse id, value
        cluster_values = self._clustermap._map.values()
        cid = [x.id() for x in cluster_values if x.name() == "#3"][0]
        pulse_values = self._pulsemap._map.values()
        pid = [x.id() for x in pulse_values if x.name() == "random"][0]
        value = 7
        block = selector.filterWithBlock(
            self.query_all_select_dynamic(cid, pid, value),
            block
        )
        # reassign parameters to maps
        self._algorithmsmap = block._alg
        self._pulsemap = block._pul
        self._clustermap = block._clu
        self._elementmap = block._ele
        # assertion
        self.assertEqual(len(self._algorithmsmap._map.values()), 1)
        self.assertEqual(len(self._pulsemap._map), 3)
        self.assertEqual(self._pulsemap.get(pid).static(), False)
        self.assertEqual(self._pulsemap.get(pid).default(), value)
        self.assertEqual(len(self._clustermap._map), 1)
        self.assertEqual(len(self._elementmap._map), 2)

    def test_selector_warn_staticdefault(self):
        pulse_values = self._pulsemap._map.values()
        pulse = [x for x in pulse_values if x.name() == "dir"][0]
        values = [2, 20.0, "str", "up"]
        for value in values:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                block = selector.FilterBlock(
                    self._algorithmsmap,
                    self._pulsemap,
                    self._clustermap,
                    self._elementmap
                )
                block = selector.filterWithBlock(
                    self.query_pulse_static_select(pulse.id(), value),
                    block
                )
                if value == "up" or value == "down":
                    self.assertEqual(len(w), 0)
                    self.assertEqual(pulse.default(), value)
                else:
                    self.assertEqual(len(w), 1)
                    self.assertTrue(issubclass(w[-1].category, UserWarning))
                    self.assertEqual(pulse.default(), None)

    def test_selector_warn_dynamicdefault(self):
        pulse_values = self._pulsemap._map.values()
        pulse = [x for x in pulse_values if x.name() == "order"][0]
        values = [20.0, 2, "str", "up"]
        for value in values:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                # filter block
                block = selector.FilterBlock(
                    self._algorithmsmap,
                    self._pulsemap,
                    self._clustermap,
                    self._elementmap
                )
                block = selector.filterWithBlock(
                    self.query_pulse_dynamic_select(pulse.id(), value),
                    block
                )
                if type(value) is pulse.type():
                    self.assertEqual(len(w), 0)
                    self.assertEqual(pulse.default(), value)
                else:
                    self.assertEqual(len(w), 1)
                    self.assertTrue(issubclass(w[-1].category, UserWarning))
                    self.assertNotEqual(pulse.default(), value)


# Load test suites
def _suites():
    return [
        Selector_TestSequence
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
