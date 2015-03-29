#!/usr/bin/env python


# import libs
import warnings
# import classes
from analytics.algorithms.algorithmsmap import AlgorithmsMap
from analytics.algorithms.algorithm import Algorithm
from analytics.algorithms.relativecomp import RelativeComparison
import analytics.utils.misc as misc

# static algorithms map
ALGORITHMS = AlgorithmsMap()
DEFAULT_ALGORITHM = RelativeComparison()
# add algorithms to the map
ALGORITHMS.assign(DEFAULT_ALGORITHM)


class AnalyseBlock(object):
    def __init__(self, algmap, elements, pulses):
        self._elementmap = elements
        self._pulsemap = pulses
        self._algorithm = None
        self._data = {"map": algmap}
        self._isAnalysed = False


# [Public]
def analyseWithBlock(analyseBlock):
    """
        Recommended method to use for ranking elements map. Uses AnalyseBlock
        instance to save and return results.

        Args:
            analyseBlock (AnalyseBlock): analyse block

        Returns:
            AnalyseBlock: updated analyse block with map and algorithm
    """
    if analyseBlock._isAnalysed:
        return analyseBlock

    # analyse with block and reassign updated elements map
    result = analyseUsingMap(
        analyseBlock._data["map"],
        analyseBlock._elementmap,
        analyseBlock._pulsemap
    )
    analyseBlock._elementmap = result["map"]
    analyseBlock._algorithm = result["algorithm"]
    analyseBlock._isAnalysed = True
    return analyseBlock


# [Public]
def analyseUsingMap(algmap, elements, pulses, withDefault=True):
    """
        Analyses using map instead of algorithm. Selects one algorithm from
        the map provided and uses it to sort the results. "withDefault"
        flag indicates whether default algorithm is used if map is empty.

        Args:
            algmap (AlgorithmsMap): map with algorithms
            elements (ElementMap): map with elements to rank
            pulses (PulseMap): map with pulses to use for ranking
            withDefault (bool): flag to use default algorithm

        Returns:
            dict<str, obj>: algorithm and updated results map
    """
    misc.checkTypeAgainst(type(algmap), AlgorithmsMap, __file__)
    # assign algorithm
    algorithm = None
    if not algmap.isEmpty():
        if len(algmap.keys()) > 1:
            msg = "Few algorithms were specified, first one will be selected"
            warnings.warn(msg, UserWarning)
        algorithm = ALGORITHMS.get(algmap.keys()[0])
    elif withDefault:
        msg = "Nothing was specified, default algorithm will be used"
        warnings.warn(msg, UserWarning)
        # set default algorithm
        algorithm = DEFAULT_ALGORITHM
    # call "analyseUsingAlgorithm" method
    updatemap = analyseUsingAlgorithm(algorithm, elements, pulses)
    result = {"algorithm": algorithm, "map": updatemap}
    return result


# [Public]
def analyseUsingAlgorithm(algorithm, elements, pulses):
    """
        Uses algorithm to rank elements. Calls "rankResults" method that is
        impolemented in abstract class Algorithm.

        Args:
            algorithm (Algorithm): Algorithm instance to use for ranking
            elements (ElementMap): map with elements to rank
            pulses (PulseMap): map with pulses

        Returns:
            ElementMap: updated elements map
    """
    # check arguments
    misc.checkInstanceAgainst(algorithm, Algorithm, __file__)
    # rank results using algorithm
    return algorithm.rankResults(elements, pulses)
