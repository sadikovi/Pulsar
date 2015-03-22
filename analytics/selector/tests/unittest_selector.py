#!/usr/bin/env python

# import libs
import unittest
# import classes
import analytics.exceptions.exceptions as ex


class Selector_TestSequence(unittest.TestCase):
    @unittest.skip('TODO')
    def test_selector(self):
        pass

# Load test suites
def _suites():
    return [
        Selector_TestSequence
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
