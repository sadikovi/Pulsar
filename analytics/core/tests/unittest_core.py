#!/usr/bin/env python

# import libs
import unittest
import random
from types import IntType, DictType
# import classes
import analytics.utils.misc as misc
from analytics.core.dataitem as DataItem


class DataItem_TestSequence(unittest.TestCase):
    def setUp(self):
        import sys
        self._input = [
            None,
            True,
            False,
            sys.maxint,
            -sys.maxint-1,
            {},
            [],
            "abc",
            0,
            1,
            -1,
            1.23,
            -3.34,
            " string ",
            " test test test ",
            "1"
        ]
        self._iterations = 20

    def test_dataitem_init(self):
        for it in self._iterations:
            # generate random attributes
            name = random.choice(self._input)
            desc = random.choice(self._input)
            seed = random.choice(self._input)
            # create and test data item
            d = DataItem(name, desc, seed)
            id = misc.generateId(seed)
            self.assertEqual(d._id, id)
            self.assertEqual(d._name, str(name).strip())
            self.assertEqual(d._desc, str(desc).strip())

    def test_dataitem_id(self):
        for it in self._iterations:
            seed = random.choice(self._input)
            d = DataItem("test string", "test string", seed)
            id = misc.generateId(seed)
            self.assertEqual(d.id(), id)

    def test_dataitem_name(self):
        for it in self._iterations:
            name = random.choice(self._input)
            d = DataItem(name, "test string", None)
            self.assertEqual(d.name(), str(name).strip())

    def test_dataitem_desc(self):
        for it in self._iterations:
            desc = random.choice(self._input)
            d = DataItem("test string", desc, None)
            self.assertEqual(d.desc(), str(desc).strip())

    def test_dataitem_getJSON(self):
        for it in self._iterations:
            # generate random attributes
            name = random.choice(self._input)
            desc = random.choice(self._input)
            seed = random.choice(self._input)
            # create and test data item json object
            d = DataItem(name, desc, seed)
            obj = d.getJSON()
            id = misc.generateId(seed)
            self.assertEqual(type(obj), DictType)
            self.assertEqual(obj["id"], id)
            self.assertEqual(obj["name"], str(name).strip())
            self.assertEqual(obj["desc"], str(desc).strip())


class Cluster_TestSequence(unittest.TestCase):
    def test_cluster_init(self):
        pass

    def test_cluster_parent(self):
        pass

    def test_cluster_children(self):
        pass

    def test_cluster_isLeaf(self):
        pass

    def test_cluster_setParent(self):
        pass

    def test_cluster_makeLeaf(self):
        pass

    def test_cluster_addChild(self):
        pass

    def test_cluster_removeChild(self):
        pass

    def test_cluster_getJSON(self):
        pass


class Element_TestSequence(unittest.TestCase):
    pass


class Pulse_TestSequence(unittest.TestCase):
    pass


# Load test suites
def _suites():
    return [
        Attribute_TestSequence,
        Core_TestSequence,
        Map_TestSequence
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
