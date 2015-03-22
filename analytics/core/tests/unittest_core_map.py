#!/usr/bin/env python

# import libs
import unittest
import random
import sys
# import classes
import analytics.utils.misc as misc
import analytics.exceptions.exceptions as ex
from analytics.core.map.dataitemmap import DataItemMap
from analytics.core.map.elementmap import ElementMap
from analytics.core.map.clustermap import ClusterMap
from analytics.core.map.pulsemap import PulseMap
from analytics.core.dataitem import DataItem
from analytics.core.cluster import Cluster
from analytics.core.element import Element
from analytics.core.pulse import Pulse, StaticPulse, DynamicPulse
from analytics.core.attribute.dynamic import Dynamic


# some general input to test
general_input = [
    None, True, False, sys.maxint, -sys.maxint-1, {}, [],
    {"1": 1, "2": 2}, [1, 2, 3, 4, 5], "abc", 0, 1, -1, 1.23,
    -3.34, " string ", " test test test ", "1"
]

class DataItemMap_TestSequence(unittest.TestCase):
    def setUp(self):
        self._teststr = "test string"
        self._sample = "1"
        self._prior = Dynamic.ForwardPriority
        self._items = [
            DataItem(self._teststr, self._teststr),
            Cluster(self._teststr, self._teststr),
            Element(self._teststr, self._teststr),
            Pulse("#1", self._teststr, self._sample),
            StaticPulse("#2", self._teststr, self._sample),
            DynamicPulse("#3", self._teststr, self._sample, self._prior)
        ]
        self._iterations = 20

    def test_dataitemmap_init(self):
        map = DataItemMap()
        self.assertEqual(map._map, {})

    def test_dataitemmap_add(self):
        map = DataItemMap()
        for el in general_input:
            with self.assertRaises(ex.AnalyticsTypeError):
                map.add(el)
        for item in self._items:
            map.add(item)
        self.assertEqual(len(map._map.keys()), len(self._items))
        sortedIds = sorted([item.id() for item in self._items])
        self.assertEqual(sorted(map._map.keys()), sortedIds)

    def test_dataitemmap_remove(self):
        map = DataItemMap()
        for item in self._items:
            map.add(item)
        sortedIds = sorted([item.id() for item in self._items])
        for id in sortedIds:
            map.remove(id)
        self.assertEqual(map._map, {})

    def test_dataitemmap_get(self):
        map = DataItemMap()
        for item in self._items:
            map.add(item)
        for inp in general_input:
            self.assertEqual(map.get(inp), None)
            # now test default
            self.assertEqual(map.get(None, inp), inp)
        for item in self._items:
            self.assertEqual(map.get(item.id()), item)

    def test_dataitemmap_has(self):
        map = DataItemMap()
        for item in self._items:
            map.add(item)
        for inp in general_input:
            self.assertEqual(map.has(inp), False)
        for item in self._items:
            self.assertEqual(map.has(item.id()), True)


class ClusterMap_TestSequence(unittest.TestCase):
    def _clusters_root_normal(self, num):
        return [Cluster(i, i) for i in range(num)]

    def _clusters_root_unknown_parent(self, num):
        return [Cluster(i, i, Cluster(i+1, i+1)) for i in range(num)]

    def _clusters_tree_normal(self, num):
        ls = [Cluster(i, i) for i in range(num)]
        map = {}
        for _i in range(len(ls)):
            if 2*_i+1 < len(ls):
                ls[2*_i+1].setParent(ls[_i])
            if 2*_i+2 < len(ls):
                ls[2*_i+2].setParent(ls[_i])
        return ls

    def _clusters_tree_reversed(self, num):
        ls = self._clusters_tree_normal(num)
        lsrev = []
        for _i in range(len(ls)):
            lsrev.append(ls[len(ls)-1-_i])
        return lsrev

    def _clusters_chain_normal(self, num):
        ls = [Cluster(i, i) for i in range(num)]
        parent = None
        for cluster in ls:
            cluster.setParent(parent)
            parent = cluster
        return ls

    def _clusters_chain_reversed(self, num):
        ls = [Cluster(i, i) for i in range(num)]
        def parent(_i):
            if len(ls) <= _i: return None
            ls[_i].setParent(parent(_i+1))
            return ls[_i]
        parent(0)
        return ls

    def _clusters_chain_cycled(self, num):
        ls = self._clusters_chain_reversed(num)
        lslen = len(ls)
        if lslen > 1:
            last = ls[lslen-1]
            first = ls[0]
            last.setParent(first)
        return ls

    def _idmap(self, ls):
        map = {}
        for it in ls:
            map[it.id()] = []
        for it in ls:
            if it.parent() is not None and it.parent().id() in map:
                map[it.parent().id()].append(it.id())
        return map

    def _recurCheck(self, elements, _idmap):
        if elements is None:
            return None
        else:
            for r in elements:
                _idmap[r.id()] = [i.id() for i in r.children()]
                self._recurCheck(r.children(), _idmap)

    def setUp(self):
        self.map = ClusterMap()
        self.num = 20

    ##### Tests #####
    def test_clustermap_init(self):
        map = ClusterMap()
        self.assertEqual(map._map, {})
        self.assertEqual(map._waitlist, {})
        self.assertEqual(map._root, {})

    def test_clustermap_add_root_normal(self):
        # 1. root normal
        ls = self._clusters_root_normal(self.num)
        for el in ls:
            self.map.add(el)
        self.assertEqual(len(self.map._root.keys()), len(ls))
        self.assertEqual(len(self.map._map.keys()), len(ls))
        self.assertEqual(self.map._waitlist, {})

    def test_clustermap_add_root_unknown(self):
        # 2. root unknown parent
        ls = self._clusters_root_unknown_parent(self.num)
        for el in ls:
            self.map.add(el)
        self.assertEqual(len(self.map._root.keys()), len(ls))
        self.assertEqual(len(self.map._map.keys()), len(ls))
        self.assertEqual(len(self.map._waitlist.keys()), len(ls))

    def test_clustermap_add_tree_normal(self):
        # 3. tree normal
        ls = self._clusters_tree_normal(self.num)
        for el in ls:
            self.map.add(el)
        self.assertEqual(len(self.map._root.keys()), 1)
        self.assertEqual(len(self.map._map.keys()), len(ls))
        self.assertEqual(self.map._waitlist, {})
        treemap = {}; idmap = self._idmap(ls)
        self._recurCheck(self.map._root.values(), treemap)
        self.assertEqual(len(treemap.keys()), len(idmap.keys()))
        for key in treemap.keys():
            self.assertEqual(sorted(treemap[key]), sorted(idmap[key]))

    def test_clustermap_add_tree_reversed(self):
        # 4. tree reversed
        ls = self._clusters_tree_reversed(self.num)
        for el in ls:
            self.map.add(el)
        self.assertEqual(len(self.map._root.keys()), 1)
        self.assertEqual(len(self.map._map.keys()), len(ls))
        self.assertEqual(self.map._waitlist, {})
        treemap = {}; idmap = self._idmap(ls)
        self._recurCheck(self.map._root.values(), treemap)
        self.assertEqual(len(treemap.keys()), len(idmap.keys()))
        for key in treemap.keys():
            self.assertEqual(sorted(treemap[key]), sorted(idmap[key]))

    def test_clustermap_add_chain_normal(self):
        # 5. chain normal
        ls = self._clusters_chain_normal(self.num)
        for el in ls:
            self.map.add(el)
        self.assertEqual(len(self.map._root.keys()), 1)
        self.assertEqual(len(self.map._map.keys()), len(ls))
        self.assertEqual(self.map._waitlist, {})
        treemap = {}; idmap = self._idmap(ls)
        self._recurCheck(self.map._root.values(), treemap)
        self.assertEqual(len(treemap.keys()), len(idmap.keys()))
        for key in treemap.keys():
            self.assertEqual(sorted(treemap[key]), sorted(idmap[key]))

    def test_clustermap_add_chain_reversed(self):
        # 6. chain reversed
        ls = self._clusters_chain_reversed(self.num)
        for el in ls:
            self.map.add(el)
        self.assertEqual(len(self.map._root.keys()), 1)
        self.assertEqual(len(self.map._map.keys()), len(ls))
        self.assertEqual(self.map._waitlist, {})
        treemap = {}; idmap = self._idmap(ls)
        self._recurCheck(self.map._root.values(), treemap)
        self.assertEqual(len(treemap.keys()), len(idmap.keys()))
        for key in treemap.keys():
            self.assertEqual(sorted(treemap[key]), sorted(idmap[key]))

    def test_clustermap_add_chain_cycled(self):
        # 7. cycles inside the list
        ls = self._clusters_chain_cycled(self.num)
        for el in ls:
            self.map.add(el)
        self.assertEqual(len(self.map._root.keys()), 1)
        self.assertEqual(len(self.map._map.keys()), len(ls))
        self.assertEqual(self.map._waitlist, {})
        treemap = {}; idmap = self._idmap(ls)
        self._recurCheck(self.map._root.values(), treemap)
        self.assertEqual(len(treemap.keys()), len(idmap.keys()))
        for key in treemap.keys():
            self.assertEqual(sorted(treemap[key]), sorted(idmap[key]))


    def test_clustermap_remove(self):
        ls = self._clusters_tree_normal(self.num)
        for el in ls:
            self.map.add(el)
        # remove all root elements
        for el in self.map._root.values():
            self.map.remove(el.id())
            del ls[ls.index(el)]
        treemap = {}; idmap = self._idmap(ls)
        self._recurCheck(self.map._root.values(), treemap)
        self.assertEqual(len(treemap.keys()), len(idmap.keys()))
        for key in treemap.keys():
            self.assertEqual(sorted(treemap[key]), sorted(idmap[key]))

    def test_clustermap_get(self):
        ls = self._clusters_tree_normal(self.num)
        for el in ls:
            self.map.add(el)
        for el in ls:
            self.assertEqual(self.map.get(el.id()), el)
            self.assertEqual(self.map.get(el.id()*2), None)


class ElementMap_TestSequence(unittest.TestCase):
    def setUp(self):
        self._teststr = "test string"
        self._sample = "1"
        self._prior = Dynamic.ForwardPriority
        self._items = [
            DataItem(self._teststr, self._teststr),
            Cluster(self._teststr, self._teststr),
            Element(self._teststr, self._teststr),
            Pulse("#1", self._teststr, self._sample),
            StaticPulse("#2", self._teststr, self._sample),
            DynamicPulse("#3", self._teststr, self._sample, self._prior)
        ]

    def test_elementmap_add(self):
        map = ElementMap()
        for item in self._items:
            if isinstance(item, Element):
                map.add(item)
            else:
                with self.assertRaises(ex.AnalyticsTypeError):
                    map.add(item)
        elements = [i.id() for i in self._items if isinstance(i, Element)]
        self.assertEqual(sorted(map._map.keys()), sorted(elements))


class PulseMap_TestSequence(unittest.TestCase):
    def setUp(self):
        self._teststr = "test string"
        self._sample = "1"
        self._prior = Dynamic.ForwardPriority
        self._items = [
            DataItem(self._teststr, self._teststr),
            Cluster(self._teststr, self._teststr),
            Element(self._teststr, self._teststr),
            Pulse("#1", self._teststr, self._sample),
            StaticPulse("#2", self._teststr, self._sample),
            DynamicPulse("#3", self._teststr, self._sample, self._prior)
        ]

    def test_pulsemap_add(self):
        map = PulseMap()
        for item in self._items:
            if isinstance(item, Pulse):
                map.add(item)
            else:
                with self.assertRaises(ex.AnalyticsTypeError):
                    map.add(item)
        elements = [i.id() for i in self._items if isinstance(i, Pulse)]
        self.assertEqual(sorted(map._map.keys()), sorted(elements))


# Load test suites
def _suites():
    return [
        DataItemMap_TestSequence,
        ClusterMap_TestSequence,
        ElementMap_TestSequence,
        PulseMap_TestSequence
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
