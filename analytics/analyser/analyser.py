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
import warnings
# import classes
from analytics.algorithms.algorithmsmap import AlgorithmsMap
from analytics.algorithms.algorithm import Algorithm
import analytics.algorithms.relativecomp as rc
import analytics.utils.misc as misc
import analytics.datavalidation.propertiesmap as prmap
import analytics.datavalidation.resultsmap as rsmap

# static algorithms map
ALGORITMS = AlgorithmsMap()
DEFAULT_ALGORITHM = rc.RelativeComparison()
# add algorithms to the map
ALGORITMS.assign(DEFAULT_ALGORITHM)


class Analyser(object):
    """
        Analyser selects proper algorithm and keeps the map of all algorithms
        that are used by analytics.

        Attributes:
            _algorithmsmap (AlgorithmsMap): map with algorithms available
            _defaultAlgorithm (Algorithm): default algorithm to use
    """
    def __init__(self):
        self._algorithmsmap = None
        self._defaultAlgorithm = None
        self._selectedAlgorithm = None
        # prepare algorithms map
        self._prepareAlgorithms()

    # [Private]
    def _prepareAlgorithms(self):
        """
            Prepares map of algorithms. All the available algorithms should
            be listed here.

            Returns:
                AlgorithmsMap: algorithms map with available instances
        """
        # initialise map to keep algorithms
        self._algorithmsmap = AlgorithmsMap()
        # collect algorithms
        for algorithm in ALGORITMS.values():
            self._algorithmsmap.assign(algorithm)
        # set relative comparison to be default algorithm
        self._setDefaultAlgorithm(DEFAULT_ALGORITHM)

    # [Private]
    def _setDefaultAlgorithm(self, algorithm):
        """
            Sets algorithm as default algorithm to use. Instance must be an
            Algorithm subclass.

            Args:
                algorithm (Algorithm): algorithm to set as default
        """
        misc.checkInstanceAgainst(algorithm, Algorithm, __file__)
        self._defaultAlgorithm = algorithm

    # [Private]
    def _hasAlgorithmsMap(self):
        """
            Method simply checks whether _algorithmsmap property is set.

            Returns:
                bool: bool value to indicate that everything is set
        """
        misc.checkTypeAgainst(type(self._algorithmsmap), AlgorithmsMap, __file__)
        return True

    # [Public]
    def allAlgorithms(self):
        """
            Returns list of algorithms that are currently available.

            Returns:
                list<Algorithm>: list of Algorithm instances
        """
        self._hasAlgorithmsMap()
        return self._algorithmsmap.values()

    # [Public]
    def getAlgorithm(self, id):
        """
            Returns algorithm by id. If id is not found, returns None.

            Returns:
                Algorithm: algorithm with id specified
        """
        self._hasAlgorithmsMap()
        return self._algorithmsmap.get(id)

    # [Private]
    def _setSelectedAlgorithm(self, algorithm):
        """
            Sets algorithm as selected.

            Args:
                algorithm (Algorithm): algorithm that has been selected
        """
        self._selectedAlgorithm = algorithm

    # [Public]
    def getSelectedAlgorithm(self):
        """
            Returns selected algorithm. Can be None or any algorithm that has
            been selected lately. Make sure that it is not retrieved without
            calling analysing method.

            Returns:
                Algorithm: selected algorithm
        """
        return self._selectedAlgorithm

    # [Public]
    def getAlgorithmsMap(self):
        """
            Returns algorithms map.

            Returns:
                AlgorithmsMap: algorithms map
        """
        return self._algorithmsmap

    # [Public]
    def analyseUsingAlgorithm(self, algorithm, resultsMap, propertiesMap):
        """
            Uses algorithm to rank results. Calls "rankResults" method that is
            impolemented in abstract class Algorithm.

            Args:
                algorithm (Algorithm): Algorithm instance to use for ranking
                resultsMap (ResultsMap): map with results to rank
                propertiesMap (PropertiesMap): map with properties

            Returns:
                ResultsMap: updated results map
        """
        # check arguments
        misc.checkInstanceAgainst(algorithm, Algorithm, __file__)
        misc.checkTypeAgainst(type(resultsMap), rsmap.ResultsMap, __file__)
        misc.checkTypeAgainst(type(propertiesMap), prmap.PropertiesMap, __file__)
        # set selected algorithm
        self._setSelectedAlgorithm(algorithm)
        # rank results using algorithm
        return algorithm.rankResults(resultsMap, propertiesMap)

    # [Public]
    def analyseUsingMap(self, algMap, resMap, propMap, withDefault=True):
        """
            Analyses using map instead of algorithm. Selects one algorithm from
            the map provided and uses it to sort the results. "withDefault"
            flag indicates whether default algorithm is used if map is empty.

            Args:
                algMap (AlgorithmsMap): map with algorithms
                resMap (ResultsMap): map with results to rank
                propMap (PropertiesMap): map with properties to use for ranking
                withDefault (bool): flag to use default algorithm

            Returns:
                ResultsMap: updated results map
        """
        misc.checkTypeAgainst(type(algMap), AlgorithmsMap, __file__)
        # assign algorithm
        algorithm = None
        if algMap.isEmpty() and not withDefault:
            misc.raiseStandardError("No algorithm is specified", __file__)
        else:
            key = None if algMap.isEmpty() else algMap.keys()[0]
            algorithm = self.getAlgorithm(key)
        # check if algorithm is still None
        if algorithm is None:
            warnings.warn(
                "No algorithm is specified, default algorithm will be used",
                UserWarning)
            algorithm = self._defaultAlgorithm
        # call "analyseUsingAlgorithm" method
        return self.analyseUsingAlgorithm(algorithm, resMap, propMap)
