#!/usr/bin/env python

# import libs
import unittest
import random
import sys
import warnings
# import classes
import analytics.utils.misc as misc
import analytics.exceptions.exceptions as ex
import analytics.core.processor.processor as processor
from types import ListType, DictType
from analytics.core.map.dataitemmap import DataItemMap
from analytics.core.map.clustermap import ClusterMap
from analytics.core.map.elementmap import ElementMap
from analytics.core.map.pulsemap import PulseMap
from analytics.core.cluster import Cluster
from analytics.core.element import Element
from analytics.core.pulse import DynamicPulse, StaticPulse, Pulse
from analytics.core.attribute.dynamic import Dynamic
from analytics.core.attribute.feature import Feature


# some general input to test
general_input = [
    None, True, False, sys.maxint, -sys.maxint-1, {}, [],
    {"1": 1, "2": 2}, [1, 2, 3, 4, 5], "abc", 0, 1, -1, 1.23,
    -3.34, " string ", " test test test ", "1"
]

class Processor_TestSequence(unittest.TestCase):
    def setUp(self):
        self._teststr = "test string"
        self._iterations = 20
        # object lists
        self._clrobj = {"id": "#1", "name": "#1", "desc": "#1", "parent": None}
        self._elmobj = {"id": "#1", "name": "#1", "desc": "#1", "cluster": None}
        self._plsobj = {"id": "#1", "name": "#1", "desc": "#1", "sample": 1}
        # maps
        self._clustermap = ClusterMap()
        self._elementmap = ElementMap()
        self._pulsemap = PulseMap()

    def test_processor_clusterObject(self):
        for it in range(self._iterations):
            obj = random.choice(general_input)
            idmapper = random.choice(general_input)
            if type(obj) is DictType:
                with self.assertRaises(KeyError):
                    processor._processClusterObject(obj, idmapper)
            else:
                with self.assertRaises(TypeError):
                    processor._processClusterObject(obj, idmapper)
        # process object without errors
        idmapper = {}
        clr = processor._processClusterObject(self._clrobj, idmapper)
        self.assertEqual(type(clr), Cluster)
        self.assertEqual(clr.name(), self._clrobj["name"])
        self.assertEqual(clr.desc(), self._clrobj["desc"])
        self.assertEqual(clr.parent(), None)
        idmapper_obj = {self._clrobj["id"]: {"cluster": clr, "parent": None}}
        self.assertEqual(idmapper, idmapper_obj)

    def test_processor_elementObject(self):
        for it in range(self._iterations):
            obj = random.choice(general_input)
            idmapper = random.choice(general_input)
            if type(obj) is DictType:
                with self.assertRaises(KeyError):
                    processor._processElementObject(obj, idmapper)
            else:
                with self.assertRaises(TypeError):
                    processor._processElementObject(obj, idmapper)
        # process object without errors
        elm = processor._processElementObject(self._elmobj)
        self.assertEqual(type(elm), Element)
        self.assertEqual(elm.name(), self._elmobj["name"])
        self.assertEqual(elm.desc(), self._elmobj["desc"])
        self.assertEqual(elm.cluster(), None)
        self.assertEqual(elm.rank(), None)

    def test_processor_pulseObject(self):
        for it in range(self._iterations):
            obj = random.choice(general_input)
            idmapper = random.choice(general_input)
            if type(obj) is DictType:
                with self.assertRaises(KeyError):
                    processor._processPulseObject(obj, idmapper)
            else:
                with self.assertRaises(TypeError):
                    processor._processPulseObject(obj, idmapper)
        # process object without errors
        pls = processor._processPulseObject(self._plsobj)
        self.assertEqual(isinstance(pls, Pulse), True)
        self.assertEqual(pls.name(), self._plsobj["name"])
        self.assertEqual(pls.desc(), self._plsobj["desc"])
        self.assertEqual(pls.type(), type(self._plsobj["sample"]))
        self.assertEqual(pls.store(), [])
        self.assertEqual(pls.default(), None)

    def test_processor_parseClusters(self):
        objlist = [self._clrobj, {}]
        idmapper = {}
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            processor.parseClusters(objlist, self._clustermap, idmapper)
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, UserWarning))
        self.assertEqual(len(self._clustermap._map), 1)
        self.assertEqual(len(self._clustermap._root), 1)
        clr = self._clustermap._map.values()[0]
        key = self._clrobj["id"]
        self.assertEqual(key in idmapper, True)
        self.assertEqual(idmapper[key], {"cluster":clr, "parent": None})

    def test_processor_parseElements(self):
        objlist = [self._elmobj, {}]
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            processor.parseElements(objlist, self._elementmap)
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, UserWarning))
        self.assertEqual(len(self._elementmap._map), 1)
        exm = self._elementmap._map.values()[0]
        self.assertEqual(len(exm.features()), 1)
        self.assertEqual(exm.features()[0].name(), "id")

    def test_processor_parsePulses(self):
        objlist = [self._plsobj, {}]
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            processor.parsePulses(objlist, self._pulsemap)
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, UserWarning))
        self.assertEqual(len(self._pulsemap._map), 1)

    def test_processor_processBlock(self):
        clusters = {"map": self._clustermap, "data": [self._clrobj]}
        elements = {"map": self._elementmap, "data": [self._elmobj]}
        pulses = {"map": self._pulsemap, "data": [self._plsobj]}
        # fill block
        block = processor.ProcessBlock(clusters, elements, pulses)
        self.assertEqual(block._clustermap, self._clustermap)
        self.assertEqual(block._elementmap, self._elementmap)
        self.assertEqual(block._pulsemap, self._pulsemap)
        self.assertEqual(block._isProcessed, False)
        # process block
        block = processor.processWithBlock(block)
        self.assertEqual(block._isProcessed, True)
        self.assertEqual(
            len(block._clustermap._map.values()), len(clusters["data"])
        )
        self.assertEqual(
            len(block._elementmap._map.values()), len(elements["data"])
        )
        self.assertEqual(
            len(block._pulsemap._map.values()), len(pulses["data"])
        )

# Load test suites
def _suites():
    return [
        Processor_TestSequence
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
