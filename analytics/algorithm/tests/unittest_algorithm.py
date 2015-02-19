# import libs
import unittest
# import classes
import analytics.exceptions.exceptions as c
import analytics.algorithm.algorithm as a

class Algorithm_TestsSequence(unittest.TestCase):
    def setUp(self):
        self.isStarted = True

    def test_algorithm_getById(self):
        with self.assertRaises(c.CheckError):
            a.Algorithm.getById(123)
        with self.assertRaises(c.CheckError):
            a.Algorithm.getById(None)
        self.assertEqual(a.Algorithm.getById("0-0-1"), a.Algorithm.ALGORITHMS_LIST[0])

    def test_algorithm_existsId(self):
        self.assertEqual(a.Algorithm.existsId("0"), False)
        self.assertEqual(a.Algorithm.existsId("0-0-1"), True)

    def test_algorithm_getByName(self):
        with self.assertRaises(c.CheckError):
            a.Algorithm.getByName(123)
        with self.assertRaises(c.CheckError):
            a.Algorithm.getByName(None)
        self.assertEqual(a.Algorithm.getByName("Relative comparison"), a.Algorithm.ALGORITHMS_LIST[0])

    def test_algorithm_existsName(self):
        self.assertEqual(a.Algorithm.existsName("0"), False)
        self.assertEqual(a.Algorithm.existsName("Relative comparison"), True)

    def test_algorithm_getByShort(self):
        with self.assertRaises(c.CheckError):
            a.Algorithm.getByShort(123)
        with self.assertRaises(c.CheckError):
            a.Algorithm.getByShort(None)
        self.assertEqual(a.Algorithm.getByShort("relative_comparison"), a.Algorithm.ALGORITHMS_LIST[0])

    def test_algorithm_existsId(self):
        self.assertEqual(a.Algorithm.existsShort("0"), False)
        self.assertEqual(a.Algorithm.existsShort("relative_comparison"), True)

# Load test suites
def _suites():
    return [
        Algorithm_TestsSequence
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
