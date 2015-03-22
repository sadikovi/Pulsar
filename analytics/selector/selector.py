#!/usr/bin/env python

# import libs
from types import StringType, ListType
import warnings
# import classes
import analytics.utils.queryengine as q
import analytics.utils.misc as misc
from analytics.algorithms.algorithmsmap import AlgorithmsMap
from analytics.core.map.clustermap import ClusterMap
from analytics.core.map.elementmap import ElementMap
from analytics.core.map.pulsemap import PulseMap


# some of the tables to use for filtering
CLUSTERS = "CLUSTERS"
ELEMENTS = "ELEMENTS"
PULSES = "PULSES"
ALGORITHMS = "ALGORITHMS"

class FilterBlock(object):
    """
        Simple class to update maps in batch.

        Attributes:
            _alg (AlgorithmsMap): map of algorithms
            _pul (PulseMap): map of pulses
            _clu (ClusterMap): map of clusters
            _ele (ElementMap): map of elements
            _isFiltered (bool): flag to show that filter block is filtered
    """
    def __init__(self, algorithmsmap, pulsemap, clustermap, elementmap):
        self._alg = algorithmsmap
        self._pul = pulsemap
        self._clu = clustermap
        self._ele = elementmap
        self._isFiltered = False

# [Public]
def filterWithBlock(queryset, flrblock):
    """
        Recommended method for filtering maps with queryset. Takes care of
        filtering order and overall process.

        Args:
            queryset (str): query set
            flrblock (FilterBlock): filter block with maps
    """
    # check if filter block has already been filtered
    if flrblock._isFiltered:
        return flrblock
    # extract query blocks
    blocks = parseQueryset(queryset, q.QueryEngine())
    if not blocks:
        return flrblock
    # filter blocks to match maps
    ablock = None; pblock = None; cblock = None
    for block in blocks:
        if block._statement._table.upper() == ALGORITHMS:
            ablock = block
        elif block._statement._table.upper() == PULSES:
            pblock = block
        elif block._statement._table.upper() == CLUSTERS:
            cblock = block
    # use each block to parse map
    flrblock._alg = filterAlgorithms(ablock, flrblock._alg)
    flrblock._pul = filterPulses(pblock, flrblock._pul)
    flrblock._clu = filterClusters(cblock, flrblock._clu)
    flrblock._ele = filterElements(flrblock._ele, flrblock._clu, flrblock._pul)
    # finished filtering
    flrblock._isFiltered = True
    return flrblock

# [Public]
def parseQueryset(queryset=None, engine=None):
    """
        Parsing query set. If query set is None or not a string, query set is
        reset to empty string. If query set is invalid, exception is thrown.

        Args:
            queryset (str): query set
            engine (QueryEngine): query engine to parse queryset

        Returns:
            list<QueryBlock>: list of query blocks
    """
    if queryset is None:
        queryset = ""
    elif type(queryset) is not StringType:
        msg = "Queryset is not a string and will be reset to empty"
        warnings.warn(msg, UserWarning)
        queryset = ""
    else:
        queryset = queryset.strip()
    # query blocks
    blocks = []
    # check if queryset is empty, and in this case return empty list
    if queryset == "":
        blocks = []
    else:
        # return query blocks
        engine = engine if type(engine) is q.QueryEngine else q.QueryEngine()
        blocks = engine.parse(queryset)
    return blocks

# [Public]
def filterAlgorithms(queryblock, algorithmsmap):
    """
        Filters algorithms.

        Args:
            queryblock (QueryBlock): query block for algorithms
            algorithmsmap (AlgorithmsMap): map of algorithms

        Returns:
            AlgorithmsMap: reference to updated algorithms map
    """
    # if queryblock is None then do not filter at all
    if queryblock is None:
        return algorithmsmap
    misc.checkTypeAgainst(type(queryblock), q.QueryBlock, __file__)
    misc.checkTypeAgainst(type(algorithmsmap), AlgorithmsMap, __file__)
    # get predicates
    predicates = queryblock._predicates
    # algorithm keys
    akeys = []
    for predicate in predicates:
        ptype = predicate._type
        parameter = predicate._parameter
        values = predicate._values
        # check only equal predicates with parameter "id"
        if ptype == q._PREDICATE_TYPES.EQUAL and parameter.upper() == "ID":
            keys.append(values[0])
    # remove keys that are not selected
    for key in algorithmsmap.keys():
        if key not in akeys:
            algorithmsmap.remove(key)
    return algorithmsmap

# [Public]
def filterPulses(queryblock, pulsemap):
    """
        Filters pulses.

        Args:
            queryblock (QueryBlock): query block for pulses
            pulsemap (PulseMap): map of pulses

        Returns:
            PulseMap: reference to updated pulses map
    """
    # if queryblock is None then do not filter at all
    if queryblock is None:
        return pulsemap
    misc.checkTypeAgainst(type(queryblock), q.QueryBlock, __file__)
    misc.checkTypeAgainst(type(pulsemap), PulseMap, __file__)
    # get predicates
    predicates = queryblock._predicates
    # check assign predicates first
    for predicate in predicates:
        ptype = predicate._type
        if ptype == _PREDICATE_TYPES.ASSIGN:
            values = predicate._values
            pulse = pulsemap.get(predicate._parameter)
            if pulse is not None and type(pulse) is DynamicPulse:
                pulse.setStatic(not values[0].upper()=="DYNAMIC")
    # check equal predicate
    for predicate in predicates:
        ptype = predicate._type
        # check equal predicate
        if ptype == q._PREDICATE_TYPES.EQUAL:
            pulse = pulsemap.get(predicate._parameter)
            if pulse is not None:
                values = predicate._values
                pulse.setDefault(values[0])
    # return updated pulsemap
    return pulsemap

# [Public]
def filterClusters(queryblock, clustermap):
    """
        Filters clusters.

        Args:
            queryblock (QueryBlock): query block for clusters
            clustermap (ClusterMap): map of clusters

        Returns:
            ClusterMap: reference to updated clusters map
    """
    # if queryblock is None then do not filter at all
    if queryblock is None:
        return clustermap
    misc.checkTypeAgainst(type(queryblock), q.QueryBlock, __file__)
    misc.checkTypeAgainst(type(clustermap), ClusterMap, __file__)
    # storing clusters
    clusters = []
    # get predicates
    predicates = queryblock._predicates
    for predicate in predicates:
        ptype = predicate._type
        parameter = predicate._parameter
        if ptype == q._PREDICATE_TYPES.EQUAL and parameter.upper() == "ID":
            if clustermap.has(values[0]):
                clusters.append(values[0])
    # filter clusters
    updatedmap = ClusterMap()
    for key in clusters:
        updatedmap.add(clustermap.get(key))
    # return updated cluster map
    return updatedmap

# [Public]
def filterElements(elementmap, clustermap, pulsemap):
    """
        Filters elements using cluster map and pulse map.

        Args:
            elementmap (ElementMap): map of elements
            clustermap (ClusterMap): filtered map of clusters
            pulsemap (PulseMap): filtered map of pulses

        Returns:
            ElementMap: reference to updated element map
    """
    misc.checkTypeAgainst(type(elementmap), ElementMap, __file__)
    misc.checkTypeAgainst(type(clustermap), ClusterMap, __file__)
    misc.checkTypeAgainst(type(pulsemap), PulseMap, __file__)
    # filter by clusters
    elements = elementmap._map.values()
    for element in elements:
        parent = element.parent()
        if parent is None or not clustermap.has(parent.id()):
            elementmap.remove(element.id())
    # filter by pulses
    elements = elementmap._map.values()
    # pulses
    # "is selectable" closure
    def isselectable(x):
        if type(x) is DynamicPulse and x.static() is True:
            return True if x.default() is not None else False
        elif type(x) is StaticPulse:
            return True if x.default() is not None else False
        else:
            return False
    pulses = [x for x in pulsemap._map.values() if isselectable(x)]
    for element in elements:
        remove = False
        for pulse in pulses:
            feature = element._features[pulse.id()]
            if feature is None or feature.value() != pulse.default():
                removed = True
        if remove:
            elementmap.remove(element.id())
    # return element map
    return elementmap
