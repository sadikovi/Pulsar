#!/usr/bin/env python

# import libs
import unittest
from types import IntType, DictType
import random
# import classes
import analytics.utils.mics as misc
from analytics.core.attribute.dynamic import Dynamic
from analytics.core.attribute.feature import Feature


class Dynamic_TestSequence(unittest.TestCase):
    def setUp(self):
        self._input = [
            None,
            True,
            False,
            sys.maxint,
            -sys.maxint-1,
            {},
            [],
            "test string",
            0,
            1,
            -1,
            1.23,
            -3.34,
            " test string ",
            " ",
            "1",
            Dynamic.ForwardPriority,
            Dynamic.ReversedPriority
        ]

    def test_dynamic_init(self):
        for el in self._input:
            obj = Dynamic(el)
            if type(el) is IntType:
                if el == Dynamic.ForwardPriority:
                    self.assertEqual(obj._priority, Dynamic.ForwardPriority)
                else:
                    self.assertEqual(obj._priority, Dynamic.ReversedPriority)
            else:
                self.assertEqual(obj._priority, Dynamic.ForwardPriority)

    def test_dynamic_priority(self):
        for el in self._input:
            obj = Dynamic(el)
            self.assertEqual(obj.priority(), obj._priority)


class Feature_TestSequence(unittest.TestCase):
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
            "test string",
            0,
            1,
            -1,
            1.23,
            -3.34,
            " test string ",
            " ",
            "1"
        ]
        self._iterations = 20

    def test_feature_init(self):
        for it in self._iterations:
            # generate attributes
            name = random.choice(self._input)
            desc = random.choice(self._input)
            value = random.choice(self._input)
            # create Feature and test it
            f = Feature(name, desc, value)
            seed = str(name).strip() + type(value).__name__
            id = misc.generateId(seed)
            self.assertEqual(f._id, id)
            self.assertEqual(f._name, str(name).strip())
            self.assertEqual(f._desc, str(desc).strip())
            self.assertEqual(f._value, value)
            self.assertEqual(f._type, type(value))

    def test_feature_value(self):
        for it in self._iterations:
            # generate attribute value
            value = random.choice(self._input)
            # create feature and test parameter
            f = Feature("test feature", "test feature", value)
            self.assertEqual(f.value(), value)

    def test_feature_type(self):
        for it in self._iterations:
            # generate attribute value
            value = random.choice(self._input)
            # create feature and test parameter
            f = Feature("test feature", "test feature", value)
            self.assertEqual(f.type(), type(value))

    def test_feature_getJSON(self):
        for it in self._iterations:
            # generate attributes
            name = random.choice(self._input)
            desc = random.choice(self._input)
            value = random.choice(self._input)
            # create feature and test parameter
            f = Feature(name, desc, value)
            json = f.getJSON()
            self.assertEqual(type(json), DictType)
            self.assertEqual(json["id"], f._id)
            self.assertEqual(json["name"], str(name).strip())
            self.assertEqual(json["desc"], str(desc).strip())
            self.assertEqual(json["value"], value)
            self.assertEqual(json["type"], type(value).__name__)


# Load test suites
def _suites():
    return [
        Dynamic_TestSequence,
        Feature_TestSequence
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
