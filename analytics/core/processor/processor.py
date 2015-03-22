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
                cluster.setParent(None)
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
    for obj in objlist:
        element = None
        try:
            element = _processElementObject(obj, idmapper)
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
    return idmapper

### Parsing pulses
# [Public]
def parsePulses(objlist, pulsemap, idmapper={}):
    """
        Parses clusters using objects list, pulse map and idmapper.

        Args:
            objlist (list<dict>): list of objects to parse into clusters
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
    cluster = Cluster(name, desc)
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
    name = obj["name"]
    desc = obj["desc"]
    clid = obj["cluster"]
    cluster = idmapper[clid]["cluster"] if clid in idmapper else None
    # leave rank as None
    rank = None
    element = Element(name, desc, cluster, rank)
    # search features
    reserved = ["name", "desc", "cluster"]
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
