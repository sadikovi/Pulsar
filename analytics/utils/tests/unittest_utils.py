# import libs
import unittest
# import classes
import analytics.exceptions.checkerror as c
import analytics.utils.hqueue as hq

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

# Load test suites
def _suites():
    return [
        hQueue_TestsSequence
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
