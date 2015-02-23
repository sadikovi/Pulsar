# import sys and update path
import sys

DIR_PATH = "/Users/sadikovi/Developer/Pulsar"
sys.path.append(DIR_PATH)

# import libs
import unittest
# import classes
import analytics.exceptions.tests.unittest_exceptions as unittest_exceptions
import analytics.datavalidation.tests.unittest_validation as unittest_validation
import analytics.loading.tests.unittest_loading as unittest_loading
import analytics.utils.tests.unittest_utils as unittest_utils
import analytics.algorithms.tests.unittest_algorithms as unittest_algorithms
import analytics.utils.tests.unittest_queryengine as unittest_queryengine
import analytics.selector.tests.unittest_selector as unittest_selector
import analytics.errorhandler.tests.unittest_errorhandling as unittest_errorhandling

def _collectSystemTests(suites):
    # exceptions
    suites.addTest(unittest_exceptions.loadSuites())
    # datavalidation
    suites.addTest(unittest_validation.loadSuites())
    # loading
    suites.addTest(unittest_loading.loadSuites())
    # utils
    suites.addTest(unittest_utils.loadSuites())
    # algorithms
    suites.addTest(unittest_algorithms.loadSuites())
    # query engine
    suites.addTest(unittest_queryengine.loadSuites())
    # selector
    suites.addTest(unittest_selector.loadSuites())
    # error handler
    suites.addTest(unittest_errorhandling.loadSuites())

if __name__ == '__main__':
    suites = unittest.TestSuite()
    _collectSystemTests(suites)
    print ""
    print "### [:Analytics] Running tests ###"
    print "-" * 70
    unittest.TextTestRunner(verbosity=2).run(suites)
