#!/usr/bin/env python

# import libs
from types import ListType, DictType, IntType, FloatType
import warnings
# import classes
import analytics.utils.misc as misc
from analytics.core.map.dataitemmap import DataItemMap
from analytics.core.map.clustermap import ClusterMap
from analytics.core.map.elementmap import ElementMap
from analytics.core.map.pulsemap import PulseMap
from analytics.core.cluster import Cluster
from analytics.core.element import Element
from analytics.core.pulse import DynamicPulse, StaticPulse
from analytics.core.attribute.dynamic import Dynamic
from analytics.core.attribute.feature import Feature


# unknown cluster for elements with parent = None
UNKNOWN_CLUSTER = Cluster(None, "Unknown", "Unknown Cluster")


class ProcessBlock(object):
    """
        Simple class to process maps in batch.

        Attributes:
            _clustermap (ClusterMap): map of clusters
            _pulsemap (PulseMap): map of pulses
            _elementmap (ElementMap): map of elements
            _isProcessed (bool): flag to show that block is processed
    """
    def __init__(self, clusters, elements, pulses, discovery=False):
        self._clustermap = clusters["map"]
        self._elementmap = elements["map"]
        self._pulsemap = pulses["map"]
        self._data = {
            "clusters": clusters["data"],
            "elements": elements["data"],
            "pulses": pulses["data"]
        }
        self._isDiscovery = bool(discovery)
        self._isProcessed = False

# [Public]
def processWithBlock(block):
    """
        Uses ProcessBlock instance to parse lists into maps. Establishes
        process of parsing by itself making it safer to use.

        Args:
            block (ProcessBlock): process block

        Returns:
            ProcessBlock: updated block
    """
    if block._isProcessed:
        return processBlock
    # util map
    idmapper = {}
    # parse object lists
    ## clusters
    idmapper = parseClusters(
        block._data["clusters"],
        block._clustermap,
        idmapper
    )
    ## elements
    idmapper = parseElements(
        block._data["elements"],
        block._elementmap,
        idmapper
    )
    ## pulses
    ### if discovery is true we try searching elements for pulses
    if block._isDiscovery:
        block._data["pulses"] = _createPulseObjects(block._elementmap)
    idmapper = parsePulses(
        block._data["pulses"],
        block._pulsemap,
        idmapper
    )
    ## check if there is any None parents in elements
    assignUnknownCluster(block._clustermap, block._elementmap)
    # block is processed
    block._isProcessed = True
    # return block
    return block

### Parsing clusters
# [Public]
def parseClusters(objlist, clustermap, idmapper={}):
    """
        Parses clusters using objects list, cluster map and idmapper.

        Args:
            objlist (list<dict>): list of objects to parse into clusters
            clustermap (ClusterMap): map to add clusters
            idmapper (dict<str, obj>):  util dictionary

        Returns:
            dict<str, obj>: util dictionary to use later
    """
    misc.checkTypeAgainst(type(objlist), ListType, __file__)
    misc.checkTypeAgainst(type(clustermap), ClusterMap, __file__)
    misc.checkTypeAgainst(type(idmapper), DictType, __file__)
    # number of failed clusters
    parse_failures = 0
    for obj in objlist:
        # parse cluster object
        try:
            _processClusterObject(obj, idmapper)
        except:
            # TODO: do not forget to log it!
            parse_failures += 1
    # try assigning parents to clusters
    # assigning failures
    assign_failures = 0
    for key in idmapper.keys():
        try:
            cluster = idmapper[key]["cluster"]
            paid = idmapper[key]["parent"]
            # make sure that paid exists and is in map
            if paid is not None and paid in idmapper:
                parent = idmapper[paid]["cluster"]
                cluster.setParent(parent)
        except:
            # TODO: do not forget to log it!
            assign_failures += 1
    # push them into map
    for key in idmapper.keys():
        clustermap.add(idmapper[key]["cluster"])
    # see if there is anything failed
    if parse_failures > 0:
        msg = "%d cluster entries could not be parsed" %(parse_failures)
        warnings.warn(msg, UserWarning)
    if assign_failures > 0:
        msg = "%d failures to assign cluster parent" %(assign_failures)
        warnings.warn(msg, UserWarning)
    # return idmapper to use it later
    return idmapper

### Parsing elements
# [Public]
def parseElements(objlist, elementmap, idmapper={}):
    """
        Parses elements using objects list, element map and idmapper.

        Args:
            objlist (list<dict>): list of objects to parse into clusters
            elementmap (ElementMap): map to add clusters
            idmapper (dict<str, obj>):  util dictionary

        Returns:
            dict<str, obj>: util dictionary to use later
    """
    misc.checkTypeAgainst(type(objlist), ListType, __file__)
    misc.checkTypeAgainst(type(elementmap), ElementMap, __file__)
    misc.checkTypeAgainst(type(idmapper), DictType, __file__)
    # failures
    parse_failures = 0
    # parse elements
    # map for values
    valmap = {}
    for obj in objlist:
        element = None
        try:
            element = _processElementObject(obj, idmapper)
            # fill value map
            for feature in element.features():
                if feature.id() in valmap:
                    valmap[feature.id()].append(feature.value())
                else:
                    valmap[feature.id()] = [feature.value()]
        except:
            # TODO: do not forget to log it!
            parse_failures += 1
        # add element to map if it is defined
        if element is not None:
            elementmap.add(element)
    # see if there is anything failed
    if parse_failures > 0:
        msg = "%d element entries could not be parsed" %(parse_failures)
        warnings.warn(msg, UserWarning)
    # return idmapper
    return valmap

### Parsing pulses
# [Public]
def parsePulses(objlist, pulsemap, idmapper={}):
    """
        Parses clusters using objects list, pulse map and idmapper.

        Args:
            objlist (list<dict>): list of objects to parse into pulses
            clustermap (PulseMap): map to add clusters
            idmapper (dict<str, obj>):  util dictionary

        Returns:
            dict<str, obj>: util dictionary to use later
    """
    misc.checkTypeAgainst(type(objlist), ListType, __file__)
    misc.checkTypeAgainst(type(pulsemap), PulseMap, __file__)
    misc.checkTypeAgainst(type(idmapper), DictType, __file__)
    # failures
    parse_failures = 0
    # parse pulse objects
    for obj in objlist:
        pulse = None
        try:
            pulse = _processPulseObject(obj, idmapper)
            # add value to store from idmapper
            if pulse.id() in idmapper:
                for vl in idmapper[pulse.id()]:
                    pulse.addValueToStore(vl)
        except:
            # TODO: do not forget to log it!
            parse_failures += 1
        # add not None pulse to map
        if pulse is not None:
            pulsemap.add(pulse)
    if parse_failures > 0:
        msg = "%d pulse entries could not be parsed" %(parse_failures)
        warnings.warn(msg, UserWarning)
    # return idmapper
    return idmapper


### Checking elements for None parent
def assignUnknownCluster(clustermap, elementmap):
    """
        Assigns unknown cluster to the element, if parent is None.

        Args:
            clustermap (ClusterMap): cluster map
            elementmap (ElementMap): element map
    """
    misc.checkTypeAgainst(type(clustermap), ClusterMap, __file__)
    misc.checkTypeAgainst(type(elementmap), ElementMap, __file__)
    for element in elementmap._map.values():
        if element.cluster() is None:
            element._cluster = UNKNOWN_CLUSTER
            if not clustermap.has(UNKNOWN_CLUSTER.id()):
                clustermap.add(UNKNOWN_CLUSTER)


### Processing functions
# [Private]
def _processClusterObject(obj, idmapper={}):
    """
        Function to process dictionary into cluster object.

        Args:
            obj (dict<str, obj>): object to parse
            idmapper (dict<str, obj>): util dictionary

        Returns:
            Cluster: cluster instance from object
    """
    # extract object properties
    uuid = obj["id"]
    name = obj["name"]
    desc = obj["desc"]
    paid = obj["parent"]
    cluster = Cluster(uuid, name, desc)
    # put data into idmapper
    idmapper[uuid] = {"cluster": cluster, "parent": paid}
    return cluster

# [Private]
def _processElementObject(obj, idmapper={}):
    """
        Function to process dictionary into element object.

        Args:
            obj (dict<str, obj>): object to parse
            idmapper (dict<str, obj>): util dictionary

        Returns:
            Element: cluster instance from object
    """
    # extract object properties
    uuid = obj["id"]
    name = obj["name"]
    desc = obj["desc"]
    clid = obj["cluster"]
    cluster = idmapper[clid]["cluster"] if clid in idmapper else None
    # leave rank as default
    element = Element(uuid, name, desc, cluster)
    # search features
    reserved = ["id", "name", "desc", "cluster"]
    for key in obj.keys():
        if key not in reserved:
            element.addFeature(Feature(key, key, obj[key]))
    return element

# [Private]
def _processPulseObject(obj, idmapper={}):
    """
        Function to process dictionary into pulse object.

        Args:
            obj (dict<str, obj>): object to parse
            idmapper (dict<str, obj>): util dictionary

        Returns:
            Pulse: cluster instance from object
    """
    # extract object properties
    name = obj["name"]
    desc = obj["desc"]
    sample = obj["sample"]
    # dynamic property only numeric
    dynamic = type(sample) in [IntType, FloatType]
    # decide what type of Pulse to create
    if dynamic:
        pr = obj["priority"] if "priority" in obj else Dynamic.ForwardPriority
        st = not bool(obj["dynamic"]) if "dynamic" in obj else True
        return DynamicPulse(name, desc, sample, pr, st)
    else:
        return StaticPulse(name, desc, sample)

# [Private]
def _createPulseObjects(elementmap):
    """
        Returns list of objects for creating pulses.

        Args:
            elementmap (ElementMap): map of elements

        Returns:
            list<obj>: list of objects to create pulses
    """
    misc.checkTypeAgainst(type(elementmap), ElementMap, __file__)
    msg = "Hmmm, though pulses are not specified, system discovered some"
    warnings.warn(msg, UserWarning)
    # list of maps to build pulses
    mp = {}
    for element in elementmap._map.values():
        for feature in element.features():
            if feature.id() not in mp:
                obj = {
                    "id": feature.id(),
                    "name": feature.name(),
                    "desc": feature.desc(),
                    "sample": feature.value()
                }
                if feature.type() in [IntType, FloatType]:
                    obj["dynamic"] = True
                    obj["priority"] = 1
                mp[feature.id()] = obj
    return mp.values()


# [Public]
def sortElements(elementlist, lowRanksFirst=False):
    """
        Sorts elements in elementmap with specified order.

        Args:
            elementlist (list<ElementMap>): elements list
            highRanksFirst (bool): flag showing the order of ranking

        Returns:
            list<Elementmap>: sorted element list
    """
    # comparison function
    def elemcmp(x, y):
        xrank = x.rank(); yrank = y.rank()
        if xrank is None or yrank is None:
            misc.raiseStandardError("Element does not have a rank", __file__)
        if xrank._value < yrank._value:
            return 1
        elif xrank._value > yrank._value:
            return -1
        else:
            return 0
    # check element list
    if len(elementlist) <= 1:
        return elementlist
    else:
        return sorted(elementlist, elemcmp, None, lowRanksFirst)
