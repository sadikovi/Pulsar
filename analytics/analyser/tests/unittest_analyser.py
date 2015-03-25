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
from types import ListType
import warnings
# import classes
import analytics.exceptions.exceptions as ex
import analytics.analyser.analyser as analyser
from analytics.algorithms.algorithmsmap import AlgorithmsMap
from analytics.algorithms.algorithm import Algorithm
from analytics.algorithms.relativecomp import RelativeComparison
from analytics.core.map.elementmap import ElementMap
from analytics.core.map.pulsemap import PulseMap


class Analyser_TestSequence(unittest.TestCase):
    def setUp(self):
        self.isStarted = True


# Load test suites
def _suites():
    return [
        Analyser_TestSequence
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
