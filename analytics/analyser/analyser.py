# import libs
import warnings
# import classes
from analytics.algorithms.algorithmsmap import AlgorithmsMap
from analytics.algorithms.algorithm import Algorithm
import analytics.algorithms.relativecomp as rc
import analytics.utils.misc as misc
import analytics.datavalidation.propertiesmap as prmap
import analytics.datavalidation.resultsmap as rsmap


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
        almap = AlgorithmsMap()
        # collect algorithms
        relcomp1 = rc.RelativeComparison()
        # and put them into map
        almap.assign(relcomp1)
        self._algorithmsmap = almap
        # set relcomp1 to be default algorithm
        self._setDefaultAlgorithm(relcomp1)

    # [Private]
    def _setDefaultAlgorithm(self, algorithm):
        """
            Sets algorithm as default algorithm to use. Instance must be an
            Algorithm subclass.

            Args:
                algorithm (Algorithm): algorithm to set as default
        """
        misc.checkInstanceAgainst(algorithm, Algorithm)
        self._defaultAlgorithm = algorithm

    # [Private]
    def _hasAlgorithmsMap(self):
        """
            Method simply checks whether _algorithmsmap property is set.

            Returns:
                bool: bool value to indicate that everything is set
        """
        misc.checkTypeAgainst(type(self._algorithmsmap), AlgorithmsMap)
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
        misc.checkInstanceAgainst(algorithm, Algorithm)
        misc.checkTypeAgainst(type(resultsMap), rsmap.ResultsMap)
        misc.checkTypeAgainst(type(propertiesMap), prmap.PropertiesMap)
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
        misc.checkTypeAgainst(type(algMap), AlgorithmsMap)
        # assign algorithm
        algorithm = None
        if algMap.isEmpty() and not withDefault:
            raise StandardError("No algorithm is specified")
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
