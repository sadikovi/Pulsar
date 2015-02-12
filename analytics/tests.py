# import sys and update path
import sys

DIR_PATH = "/Users/sadikovi/Developer/Pulsar"
sys.path.append(DIR_PATH)

# import libs
import unittest
# import classes
import analytics.datavalidation.tests.unittest_exceptions as unittest_exceptions
import analytics.datavalidation.tests.unittest_validation as unittest_validation

def _collectSystemTests(suites):
    # datavalidation - exceptions
    suites.addTest(unittest_exceptions.loadSuites())
    # datavlidation - validation
    suites.addTest(unittest_validation.loadSuites())

if __name__ == '__main__':
    suites = unittest.TestSuite()
    _collectSystemTests(suites)
    print ""
    print "### [:Analytics] Running tests ###"
    print "-" * 70
    unittest.TextTestRunner(verbosity=2).run(suites)
