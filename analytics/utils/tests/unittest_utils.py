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
import inspect
import uuid
from types import DictType, ListType
# import classes
import analytics.exceptions.exceptions as c
import analytics.utils.hqueue as hq
import analytics.utils.misc as misc

# Superclass for this tests sequence
class Utils_TestsSequence(unittest.TestCase):
    def setUp(self):
        self.isStarted = True

# hQueue tests
class hQueue_TestsSequence(Utils_TestsSequence):

    def setUp(self):
        self._array = [1, 2, 3, 4, 5]

    def test_hqueue_init(self):
        with self.assertRaises(c.AnalyticsCheckError):
            queue = hq.hQueue({})
        queue = hq.hQueue(self._array)
        self.assertEqual(queue._queue, self._array)

    def test_hqueue_randomize(self):
        queue = hq.hQueue(self._array)
        queue.randomize()
        queue._queue.sort()
        self.assertEqual(queue._queue, self._array)

    def test_hqueue_isEmpty(self):
        queue = hq.hQueue([])
        self.assertEqual(queue.isEmpty(), True)
        queue.enqueue(1)
        self.assertEqual(queue.isEmpty(), False)
        queue.dequeue()
        self.assertEqual(queue.isEmpty(), True)

    def test_hqueue_enqueue(self):
        queue = hq.hQueue([])
        queue.enqueue(1)
        self.assertEqual(queue._queue, [1])

    def test_hqueue_dequeue(self):
        queue = hq.hQueue([])
        queue.enqueue(1)
        queue.enqueue(2)
        queue.dequeue()
        self.assertEqual(queue._queue, [2])

    def test_hqueue_peek(self):
        queue = hq.hQueue(self._array)
        obj = queue.peek()
        self.assertEqual(obj, queue._queue[0])
        self.assertEqual(len(queue._queue), len(self._array))

    def test_hqueue_getList(self):
        queue = hq.hQueue(self._array)
        self.assertEqual(queue.getList(), self._array)

# misc tests
class misc_TestsSequence(Utils_TestsSequence):

    def test_misc_checkTypeAgainst(self):
        a = {"id":"1"}
        with self.assertRaises(c.AnalyticsCheckError):
            misc.checkTypeAgainst(type(a), ListType, __file__)
        try:
            misc.checkTypeAgainst(type(a), ListType, __file__)
        except c.AnalyticsCheckError as e:
            self.assertEqual(e._line, str(inspect.currentframe().f_lineno-2))
        t = misc.checkTypeAgainst(type(a), DictType, __file__)
        self.assertEqual(t, True)

    def test_misc_checkInstanceAgainst(self):
        class A(object):
            pass
        class B(A):
            pass
        class C(B):
            pass
        aobj = A(); bobj = B(); cobj = C()
        self.assertTrue(misc.checkInstanceAgainst(aobj, A, __file__))
        self.assertTrue(misc.checkInstanceAgainst(bobj, B, __file__))
        self.assertTrue(misc.checkInstanceAgainst(cobj, C, __file__))
        self.assertTrue(misc.checkInstanceAgainst(bobj, A, __file__))
        self.assertTrue(misc.checkInstanceAgainst(cobj, A, __file__))
        with self.assertRaises(c.AnalyticsTypeError):
            self.assertTrue(misc.checkInstanceAgainst(aobj, B, __file__))

    def test_misc_generateId(self):
        guid = misc.generateId()
        self.assertEqual(len(uuid.uuid4().hex), len(guid))
        guid = misc.generateId("test")
        self.assertEqual(uuid.uuid3(uuid.NAMESPACE_DNS, "test").hex, guid)

# Load test suites
def _suites():
    return [
        hQueue_TestsSequence,
        misc_TestsSequence
    ]

# Load tests
def loadSuites():
    #global test suite for this module
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
