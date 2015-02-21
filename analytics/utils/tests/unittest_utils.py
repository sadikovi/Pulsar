# import libs
import unittest
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
        with self.assertRaises(c.CheckError):
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
        with self.assertRaises(c.CheckError):
            misc.checkTypeAgainst(type(a), ListType)
        t = misc.checkTypeAgainst(type(a), DictType)
        self.assertEqual(t, True)

    def test_misc_checkInstanceAgainst(self):
        class A(object):
            pass
        class B(A):
            pass
        class C(B):
            pass
        a = A(); b = B(); c = C()
        self.assertTrue(misc.checkInstanceAgainst(a, A))
        self.assertTrue(misc.checkInstanceAgainst(b, B))
        self.assertTrue(misc.checkInstanceAgainst(c, C))
        self.assertTrue(misc.checkInstanceAgainst(b, A))
        self.assertTrue(misc.checkInstanceAgainst(c, A))
        with self.assertRaises(TypeError):
            self.assertTrue(misc.checkInstanceAgainst(a, B))

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
