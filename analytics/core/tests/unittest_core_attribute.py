#!/usr/bin/env python

# import libs
import unittest
from types import IntType, DictType
import random
import sys
# import classes
import analytics.utils.misc as misc
from analytics.core.attribute.dynamic import Dynamic
from analytics.core.attribute.feature import Feature


# some general input to test
general_input = [
    None, True, False, sys.maxint, -sys.maxint-1, {}, [],
    {"1": 1, "2": 2}, [1, 2, 3, 4, 5], "abc", 0, 1, -1, 1.23,
    -3.34, " string ", " test test test ", "1"
]

class Dynamic_TestSequence(unittest.TestCase):
    def test_dynamic_init(self):
        for el in general_input:
            obj = Dynamic(el)
            if type(el) is IntType:
                if el == Dynamic.ReversedPriority:
                    self.assertEqual(obj._priority, Dynamic.ReversedPriority)
                else:
                    self.assertEqual(obj._priority, Dynamic.ForwardPriority)
            else:
                self.assertEqual(obj._priority, Dynamic.ForwardPriority)

    def test_dynamic_priority(self):
        for el in general_input:
            obj = Dynamic(el)
            self.assertEqual(obj.priority(), obj._priority)


class Feature_TestSequence(unittest.TestCase):
    def setUp(self):
        self._iterations = 20
        self._teststr = "test feature"

    def test_feature_init(self):
        for it in range(self._iterations):
            # generate attributes
            name = random.choice(general_input)
            desc = random.choice(general_input)
            value = random.choice(general_input)
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
        for it in range(self._iterations):
            # generate attribute value
            value = random.choice(general_input)
            # create feature and test parameter
            f = Feature(self._teststr, self._teststr, value)
            self.assertEqual(f.value(), value)

    def test_feature_type(self):
        for it in range(self._iterations):
            # generate attribute value
            value = random.choice(general_input)
            # create feature and test parameter
            f = Feature(self._teststr, self._teststr, value)
            self.assertEqual(f.type(), type(value))

    def test_feature_getJSON(self):
        for it in range(self._iterations):
            # generate attributes
            name = random.choice(general_input)
            desc = random.choice(general_input)
            value = random.choice(general_input)
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
