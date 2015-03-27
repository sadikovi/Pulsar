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


# import os, sys and update path
import os
import sys

# set default path as an external directory of the module
DIR_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(DIR_PATH)

# import libs
import unittest

# select what tests to run
_RUN_TESTS = {
    "exceptions":       True,
    "loading":          True,
    "utils":            True,
    "algorithms":       True,
    "relcomp_alg":      True,
    "query_engine":     True,
    "selector":         True,
    "analyser":         True,
    "datamanager":      True,
    "core_attribute":   True,
    "core":             True,
    "core_map":         True,
    "core_processor":   True,
    "service":          True
}

def _checkTest(key):
    return key in _RUN_TESTS and _RUN_TESTS[key]

def _collectSystemTests(suites):
    # exceptions
    if _checkTest("exceptions"):
        import analytics.exceptions.tests.unittest_exceptions as unittest_exceptions
        suites.addTest(unittest_exceptions.loadSuites())
    else:
        print "@skip: exceptions tests"

    # loading
    if _checkTest("loading"):
        import analytics.loading.tests.unittest_loading as unittest_loading
        suites.addTest(unittest_loading.loadSuites())
    else:
        print "@skip: loading tests"

    # utils
    if _checkTest("utils"):
        import analytics.utils.tests.unittest_utils as unittest_utils
        suites.addTest(unittest_utils.loadSuites())
    else:
        print "@skip: utils tests"

    # algorithms
    if _checkTest("algorithms"):
        import analytics.algorithms.tests.unittest_algorithms as unittest_algorithms
        suites.addTest(unittest_algorithms.loadSuites())
    else:
        print "@skip: algorithms tests"

    # relative comparion algorithm
    if _checkTest("relcomp_alg"):
        import analytics.algorithms.tests.unittest_relativecomp as unittest_relativecomp
        suites.addTest(unittest_relativecomp.loadSuites())
    else:
        print "@skip: relative comparison algorithm tests"

    # query engine
    if _checkTest("query_engine"):
        import analytics.utils.tests.unittest_queryengine as unittest_queryengine
        suites.addTest(unittest_queryengine.loadSuites())
    else:
        print "@skip: query engine tests"

    # selector
    if _checkTest("selector"):
        import analytics.selector.tests.unittest_selector as unittest_selector
        suites.addTest(unittest_selector.loadSuites())
    else:
        print "@skip: selector tests"

    # analyser
    if _checkTest("analyser"):
        import analytics.analyser.tests.unittest_analyser as unittest_analyser
        suites.addTest(unittest_analyser.loadSuites())
    else:
        print "@skip: analyser tests"

    # datamanager
    if _checkTest("datamanager"):
        import analytics.datamanager.tests.unittest_datamanager as unittest_datamanager
        suites.addTest(unittest_datamanager.loadSuites())
    else:
        print "@skip: data manager tests"

    # core attributes
    if _checkTest("core_attribute"):
        import analytics.core.tests.unittest_core_attribute as unittest_core_attribute
        suites.addTest(unittest_core_attribute.loadSuites())
    else:
        print "@skip: core attribute tests"

    # core
    if _checkTest("core"):
        import analytics.core.tests.unittest_core as unittest_core
        suites.addTest(unittest_core.loadSuites())
    else:
        print "@skip: core tests"

    # core maps
    if _checkTest("core_map"):
        import analytics.core.tests.unittest_core_map as unittest_core_map
        suites.addTest(unittest_core_map.loadSuites())
    else:
        print "@skip: core map tests"

    # core processor
    if _checkTest("core_processor"):
        import analytics.core.tests.unittest_core_processor as unittest_core_processor
        suites.addTest(unittest_core_processor.loadSuites())
    else:
        print "@skip: core processor tests"

    # service
    if _checkTest("service"):
        import analytics.tests.unittest_service as unittest_service
        suites.addTest(unittest_service.loadSuites())
    else:
        print "@skip: service tests"

if __name__ == '__main__':
    suites = unittest.TestSuite()
    print ""
    print "### [:Analytics] Gathering tests info ###"
    print "-" * 70
    _collectSystemTests(suites)
    print ""
    print "### [:Analytics] Running tests ###"
    print "-" * 70
    unittest.TextTestRunner(verbosity=2).run(suites)
    num = len([x for x in _RUN_TESTS.values() if not x])
    print "%s Number of test blocks skipped: %d" %("OK" if num==0 else "WARN", num)
    print ""
