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
from types import StringType, ListType
import os
import warnings
import sys
import traceback
# import classes
import analytics.exceptions.exceptions as ex
import analytics.utils.misc as misc
import projectpaths as paths
import analytics.datamanager.datamanager as datamanager
import analytics.core.processor.processor as processor
import analytics.selector.selector as selector
import analytics.analyser.analyser as analyser
from analytics.loading.loader import Loader
from analytics.loading.jsonloader import JsonLoader
from analytics.loading.xmlloader import XmlLoader
from analytics.core.map.clustermap import ClusterMap
from analytics.core.map.elementmap import ElementMap
from analytics.core.map.pulsemap import PulseMap
from analytics.algorithms.algorithmsmap import AlgorithmsMap
import analytics.log as log


# if it runs tests - set True
IS_TEST = False

# Authorised email list
#[Private]
EMAIL_LIST = [
    "test@example.com"
]

# datamanager
_datamanager = datamanager.DataManager()
_datamanager.setSearchPath(paths.DATASETS_PATH)
# load all datasets
_datamanager.loadDatasets()


# [Public]
def isUserInEmaillist(email):
    """
        Returns boolean value that indicates the user email in authorised
        email list.

        Args:
            email (str): user email

        Returns:
            bool: indicator whether email in email list
    """
    return email in EMAIL_LIST


# [Private]
def searchDatasets(dmngr=None):
    """
        Searches and returns raw list of datasets.

        Args:
            dmngr (DataManager): datamanager specified

        Returns:
            list<Dataset>: list of datasets
    """
    dmngr = dmngr or _datamanager
    return dmngr.getDatasets()


# [Public]
def getAllDatasets():
    """
        Returns list with all datasets available. If something fails, return
        empty list.

        Returns:
            dict<str, obj>: list of available datasets
    """
    try:
        obj = [x.getJSON() for x in searchDatasets()]
        return _generateSuccessMessage([], obj)
    except BaseException as e:
        # log error
        _type, _value, _trace = sys.exc_info()
        log.logger(IS_TEST).error(traceback.format_exception(_type, _value, _trace))
        return _generateErrorMessage([str(e)])

# [Public]
# [Restrictions]
def searchDataset(datasetId, dmngr=None):
    """
        [!] Restricted use.
        Returns dataset object for dataset id. Does not return generated
        message.

        Returns:
            Dataset: dataset object
    """
    try:
        dmngr = dmngr or _datamanager
        return dmngr.getDataset(datasetId)
    except BaseException as e:
        # log error
        _type, _value, _trace = sys.exc_info()
        log.logger(IS_TEST).error(traceback.format_exception(_type, _value, _trace))
        return None


# [Public]
def requestData(datasetId, query, dmngr=None, issorted=False, iswarnings=True):
    """
        Public method to request data, has error handling. Returns data json,
        if everything is okay, otherwise returns error json.

        Args:
            datasetId (str): id of a particular dataset
            query (str): select query for data
            dmngr (DataManager): hook to pass own datamanager for tests
            issorted (bool): indicates whether elements are sorted or not
            iswarnings (bool): indicates wherther warnings are reported or not

        Returns:
            dict<str, obj>: json object of results
    """
    jsonobj = {}
    try:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # retrieve object
            obj = _getDataObject(datasetId, query, dmngr, issorted)
            # 30.03.2015 ivan.sadikov: added iswarnings feature
            messages = [str(wm.message) for wm in w] if iswarnings else []
            # prepare json object
            jsonobj = _generateSuccessMessage(messages, obj)
            # log warnings
            for wm in w:
                log.logger(IS_TEST).warn(wm.message)
    except ex.AnalyticsBaseException as e:
        jsonobj = _generateErrorMessage([e._errmsg])
        # log error
        _type, _value, _trace = sys.exc_info()
        log.logger(IS_TEST).error(traceback.format_exception(_type, _value, _trace))
    except BaseException as be:
        jsonobj = _generateErrorMessage([str(be)])
        # log error
        _type, _value, _trace = sys.exc_info()
        log.logger(IS_TEST).error(traceback.format_exception(_type, _value, _trace))
    return jsonobj


# [Private]
def _getDataObject(datasetId, queryset, dmngr=None, issorted=False):
    """
        Returns data object for dataset id and queryset.

        Args:
            datasetId (str): dataset id
            queryset (str): query string
            dmngr (DataManager): hook to pass own datamanager for tests
            issorted (bool): indicates whether elements are sorted or not

        Returns:
            dict<str, obj>: object with clusters, elements, pulses, algorithm
    """
    # check arguments
    misc.checkTypeAgainst(type(datasetId), StringType, __file__)
    misc.checkTypeAgainst(type(queryset), StringType, __file__)
    # trim arguments
    datasetId = datasetId.strip(); queryset = queryset.strip();
    # find that ther is actual dataset stored
    if dmngr is None:
        dmngr = _datamanager
    dataset = dmngr.getDataset(datasetId)
    # check dataset
    if dataset is None:
        # no datasets - error
        misc.raiseStandardError("No such dataset", __file__)
    # everything is okay
    ## extract information about core elements
    cludata = dataset._clusters
    eledata = dataset._elements
    puldata = dataset._pulses
    isdiscover = dataset._discover
    ## clusters list
    clusters = _loaderForDatatype(
        cludata[datamanager.TYPE],
        cludata[datamanager.PATH]
    ).processData()
    ## elements list
    elements = _loaderForDatatype(
        eledata[datamanager.TYPE],
        eledata[datamanager.PATH]
    ).processData()
    ## pulses list (if we discover pulses skip step)
    pulses = []
    if not isdiscover:
        pulses = _loaderForDatatype(
            puldata[datamanager.TYPE],
            puldata[datamanager.PATH]
        ).processData()
    # create maps
    clustermap = ClusterMap()
    elementmap = ElementMap()
    pulsemap = PulseMap()
    # create process block and call processor
    pblock = processor.ProcessBlock(
        {"map": clustermap, "data": clusters},
        {"map": elementmap, "data": elements},
        {"map": pulsemap, "data": pulses},
        isdiscover
    )
    pblock = processor.processWithBlock(pblock)

    # create filter block and call selector
    algmap = AlgorithmsMap()
    for alg in analyser.ALGORITHMS.values():
        algmap.assign(alg)
    fblock = selector.FilterBlock(
        algmap,
        pblock._pulsemap,
        pblock._clustermap,
        pblock._elementmap
    )
    fblock = selector.filterWithBlock(queryset, fblock)
    # create analyse block and call analyser
    ablock = analyser.AnalyseBlock(fblock._alg, fblock._ele, fblock._pul)
    ablock = analyser.analyseWithBlock(ablock)
    # reassign updated maps
    clustermap = fblock._clu
    elementmap = ablock._elementmap
    pulsemap = fblock._pul
    algorithm = ablock._algorithm
    # extract json object from maps and send success message
    ## as elements now can be sorted we extract json manually
    elementlist = elementmap._map.values()
    if issorted:
        elementlist = processor.sortElements(elementlist)
    obj = {
        "clusters": clustermap.getJSON(),
        "elements": [x.getJSON() for x in elementlist],
        "pulses": pulsemap.getJSON(),
        "algorithm": algorithm.getJSON()
    }
    return obj


# [Private]
def _loaderForDatatype(datatype=None, filepath=""):
    """
        Returns Loader instance for a particular datatype. If datatype is
        unknown throws an exception.

        Args:
            datatype (str): file format of storing data (e.g. json, xml)

        Returns:
            Loader: loader instance
    """
    if datatype == "json":
        return JsonLoader.prepareDataFrom(filepath)
    elif datatype == "xml":
        return XmlLoader.prepareDataFrom(filepath)
    else:
        msg = "Unknown datatype %s" % (str(datatype))
        misc.raiseStandardError(msg, __file__)
    return None


# [Private]
def _generateSuccessMessage(messages, dataobj):
    """
        Generates success message that includes status, code, data object
        and messages list.

        Args:
            messages (list<str>): list of messages
            dataobj (dict<str, obj>): data object

        Returns:
            dict<str, obj>: json representation of success message
    """
    if type(messages) is not ListType:
        messages = [messages]
    # build global object
    obj = {
        "status": "success",
        "code": 200,
        "data": dataobj,
        "messages": messages
    }
    return obj


# [Private]
def _generateErrorMessage(messages, code=400):
    """
        Generates json with error message provided.

        Args:
            messages (list<str>): error message
            code (int): error message code

        Returns:
            dict<str, obj>: json object with error message
    """
    if type(messages) is not ListType:
        messages = [messages]
    # build global error object
    obj = {
        "code": int(code),
        "status": "error",
        "data": None,
        "messages": messages
    }
    return obj
