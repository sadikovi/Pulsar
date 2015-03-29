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
import warnings
# import classes
import analytics.exceptions.exceptions as ex
import analytics.core.processor.processor as processor
import analytics.analyser.analyser as analyser
import analytics.algorithms.rank as rnk
from analytics.algorithms.algorithmsmap import AlgorithmsMap
from analytics.algorithms.relativecomp import RelativeComparison
from analytics.core.map.elementmap import ElementMap
from analytics.core.map.pulsemap import PulseMap
from analytics.core.map.clustermap import ClusterMap


class Analyser_TestSequence(unittest.TestCase):
    def setUp(self):
        self.isStarted = True
        self._a = [
                {"name": "value", "desc": "value", "sample": 128, "dynamic": True, "priority": -1},
                {"name": "price", "desc": "price", "sample": 245.0, "dynamic": True, "priority": 1},
                {"name": "amount", "desc": "amount", "sample": 3, "dynamic": True}
        ]
        self._b = [
            {"id": "1","name": "#1","desc": "", "cluster": "A", "value": 100, "price": 320.0, "amount": 1},
            {"id": "2","name": "#2","desc": "", "cluster": "A", "value": 120, "price": 300.0, "amount": 4},
            {"id": "3","name": "#3","desc": "", "cluster": "A", "value": 140, "price": 199.0, "amount": 3},
            {"id": "4","name": "#4","desc": "", "cluster": "A", "value": 124, "price": 234.0, "amount": 5},
            {"id": "5","name": "#5","desc": "", "cluster": "A", "value": 150, "price": 250.0, "amount": 9},
            {"id": "6","name": "#6","desc": "", "cluster": "B", "value": 128, "price": 245.0, "amount": 3},
            {"id": "7","name": "#7","desc": "", "cluster": "B", "value": 125, "price": 230.0, "amount": 2}
        ]
        self._c = [
            {"id": "1", "name": "O", "desc": "O", "parent": None},
            {"id": "2", "name": "A", "desc": "A", "parent": "O"},
            {"id": "3", "name": "B", "desc": "B", "parent": "O"}
        ]
        # initialise maps and idmapper
        self.pulses = PulseMap()
        self.elements = ElementMap()
        self.clusters = ClusterMap()
        idmapper = processor.parseClusters(self._c, self.clusters, {})
        idmapper = processor.parseElements(self._b, self.elements, idmapper)
        idmapper = processor.parsePulses(self._a, self.pulses, idmapper)

    def test_analyser_analyseWithErrors(self):
        # algorithms
        algorithms = AlgorithmsMap()
        for alg in analyser.ALGORITHMS.values():
            algorithms.assign(alg)
        # run analyser
        with self.assertRaises(ex.AnalyticsTypeError):
            analyser.analyseUsingMap(
                AlgorithmsMap(),
                self.elements,
                self.pulses,
                False
            )
        # run again to catch warning
        algorithms.assign(RelativeComparison())
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # rank elements
            block = analyser.AnalyseBlock(
                algorithms,
                self.elements,
                self.pulses
            )
            block = analyser.analyseWithBlock(block)
            self.assertEqual(block._algorithm, algorithms.values()[0])
            # warnings assertion
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, UserWarning))

    def test_analyser_analyseDynamic(self):
        # algorithms
        algorithms = AlgorithmsMap()
        for alg in analyser.ALGORITHMS.values():
            algorithms.assign(alg)
        # analyse results
        block = analyser.AnalyseBlock(algorithms, self.elements, self.pulses)

        # catch warning about too many dynamic properties
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            block = analyser.analyseWithBlock(block)
            # warnings assertion
            self.assertEqual(len(w), 1)
            self.assertTrue(issubclass(w[0].category, UserWarning))

        # leave only two dynamic properties
        self.pulses._map.values()[0].setStatic(True)
        # analyse elements again
        block = analyser.analyseWithBlock(block)
        self.assertEqual(block._isAnalysed, True)
        self.assertEqual(block._algorithm, algorithms.values()[0])
        elements = block._elementmap
        for element in elements._map.values():
            self.assertNotEqual(element.rank()._name, rnk.RSYS.UND_RANK._name)

    def test_analyser_analyseStatic(self):
        # algorithms
        algorithms = AlgorithmsMap()
        for alg in analyser.ALGORITHMS.values():
            algorithms.assign(alg)
        # set all properties as static
        for pulse in self.pulses._map.values():
            pulse.setStatic(True)
        # analyse results
        block = analyser.AnalyseBlock(algorithms, self.elements, self.pulses)
        # rank elements
        block = analyser.analyseWithBlock(block)
        self.assertEqual(block._isAnalysed, True)
        self.assertEqual(block._algorithm, algorithms.values()[0])
        elements = block._elementmap
        for element in elements._map.values():
            self.assertEqual(element.rank()._name, rnk.RSYS.UND_RANK._name)


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
