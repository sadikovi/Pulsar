# import libs
import unittest
# import classes
import analytics.exceptions.exceptions as ex
import analytics.algorithms.algorithmsmap as a
import analytics.algorithms.algorithm as al


class TestAlgorithm(al.Algorithm):
    def __init__(self, id, name, short):
        self._id = id
        self._name = name
        self._short = short

    def getId(self):
        return self._id

class Algorithms_TestsSequence(unittest.TestCase):
    def setUp(self):
        self.isStarted = True

class AlgorithmsMap_TestsSequence(Algorithms_TestsSequence):

    def setUp(self):
        self._almap = a.AlgorithmsMap()

    def test_algorithmsmap_init(self):
        self.assertEqual(self._almap._map, {})

    def test_algorithmsmap_has(self):
        self.assertEqual(self._almap.has("123"), False)
        self._almap._map["123"] = []
        self.assertEqual(self._almap.has("123"), True)

    def test_algorithmsmap_assign(self):
        with self.assertRaises(TypeError):
            self._almap.assign([])

        test = TestAlgorithm("id", "name", "short")
        self._almap.assign(test)
        self.assertEqual(self._almap.has("id"), True)
        self.assertEqual(self._almap._map["id"], test)

    def test_algorithmsmap_remove(self):
        test = TestAlgorithm("id", "name", "short")
        self._almap.assign(test)
        self.assertEqual(self._almap.has("id"), True)
        self._almap.remove("id")
        self.assertEqual(self._almap.has("id"), False)

    def test_algorithmsmap_get(self):
        test = TestAlgorithm("id", "name", "short")
        self._almap.assign(test)
        self.assertEqual(self._almap.has("id"), True)
        self.assertEqual(self._almap.get("id"), test)

    def test_algorithmsmap_isEmpty(self):
        self.assertEqual(self._almap.isEmpty(), True)
        test = TestAlgorithm("id", "name", "short")
        self._almap.assign(test)
        self.assertEqual(self._almap.isEmpty(), False)
        self._almap.remove("id")
        self.assertEqual(self._almap.isEmpty(), True)

# Load test suites
def _suites():
    return [
        AlgorithmsMap_TestsSequence
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
