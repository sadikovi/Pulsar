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
import json
from types import StringType, ListType
import os
# import classes
import analytics.exceptions.exceptions as ex
import analytics.utils.misc as misc
from analytics.loading.loader import Loader
from analytics.loading.jsonloader import JsonLoader
from analytics.loading.xmlloader import XmlLoader
import analytics.datavalidation.validator as vl
import analytics.selector.selector as sl
import analytics.analyser.analyser as al
import analytics.datavalidation.groupsmap as gm
import analytics.datavalidation.resultsmap as rm
import analytics.datavalidation.propertiesmap as pm
import analytics.algorithms.algorithmsmap as am
from analytics.algorithms.algorithm import Algorithm
import analytics.datamanager.datamanager as datamanager

# project directory
ANALYTICS_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# Authorised email list
#[Private]
_EMAIL_LIST = [
    "test@example.com"
]

# datamanager
_datamanager = datamanager.DataManager()
_datamanager.setSearchPath(os.path.join(ANALYTICS_DIRECTORY, "datasets"))
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
    return email in _EMAIL_LIST if email is not None else False


# [Public]
def getAllDatasets():
    """
        Returns list with all datasets available. If something fails, return
        empty list.

        Returns:
            str: json string of available datasets
    """
    jsonstr = "[]"
    try:
        obj = [x.getJSON() for x in _datamanager.getDatasets()]
        jsonstr = json.dumps(obj)
    except:
        jsonstr = "[]"
    return jsonstr


# [Public]
def requestData(datasetId, query):
    """
        Public method to request data, has error handling. Returns data json,
        if everything is okay, otherwise returns error json.

        Args:
            datasetId (str): id of a particular dataset
            query (str): select query for data

        Returns:
            str: json string of results
    """
    jsonstring = ""
    try:
        # check arguments
        misc.checkTypeAgainst(type(datasetId), StringType, __file__)
        misc.checkTypeAgainst(type(query), StringType, __file__)
        # trim arguments
        datasetId = datasetId.strip(); query = query.strip();
        # find that ther is actual dataset stored
        dataset = _datamanager.getDataset(datasetId)
        # check dataset
        if dataset is None:
            # no datasets - error
            misc.raiseStandardError("No such dataset", __file__)
        # everything is okay
        # extract dataset and get path
        jsonobj = _requestData(dataset, query)
        jsonstring = _generateSuccessMessage(jsonobj)
    except ex.AnalyticsBaseException as e:
        jsonstring = _generateErrorMessage(e._errmsg)
    return jsonstring


# [Private]
# requesting data for dataset
def _requestData(dataset, query):
    """
        Collects data from dataset and applies query to select a particular
        results. Empty query means default selection.

        Args:
            dataset (Dataset): Dataset instance
            query (str): select query for data

        Returns:
            str: json string of results
    """
    # check parameters
    misc.checkTypeAgainst(type(dataset), datamanager.Dataset, __file__)
    misc.checkTypeAgainst(type(query), StringType, __file__)
    # prepare json objects
    groups = None; results = None; properties = None
    # create groups loader and extract data
    groupsLoader =  _loaderForDatatype(dataset._groups["type"])
    groups = groupsLoader.processData(dataset._groups["path"])
    # create results loader and extract data
    resultsLoader =  _loaderForDatatype(dataset._results["type"])
    results = resultsLoader.processData(dataset._results["path"])
    if not dataset._discover:
        propsLoader =  _loaderForDatatype(dataset._properties["type"])
        _props = propsLoader.processData(dataset._properties["path"])
    else:
        _props = []
    properties = _props
    # now we have groups, results, and properties
    # prepare instances to perform actions on data
    validator = vl.Validator()
    selector = sl.Selector()
    analyser = al.Analyser()
    # call validator to convert data into dataitems
    validator.prepareData(groups, results, properties)
    # extract maps from validator
    groupsmap = validator.getGroups()
    resmap = validator.getResults()
    propsmap = validator.getProperties()
    # get algorithms map from analyser
    algsmap = analyser.getAlgorithmsMap()
    # call selector and filter data
    selector.loadQueriesFromQueryset(query)
    selector.setSkipFiltering(True if query=="" else False)
    # check flag whether selector has performed filtering or not
    flag = selector.startFiltering(resmap, groupsmap, propsmap, algsmap)
    # analyse using algorithms map
    resmap = analyser.analyseUsingMap(algsmap, resmap, propsmap)
    # get last selected algorithm that has been used by this instance
    selectedAlg = analyser.getSelectedAlgorithm()
    # now we have everything filtered and ranked
    # prepare json object to send data back
    jsonobj = _generateDataJSON(groupsmap, resmap, propsmap,
                                    selectedAlg, al.ALGORITMS)
    return jsonobj


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


def _generateDataJSON(groupsmap, resultsmap, propertiesmap, algorithm, algsmap):
    """
        Generates json data from maps and algorithm, combines them together to
        return back.

        Args:
            groupsmap (GroupsMap): map of the groups
            resultsmap (ResultsMap): map of the results
            propsmap (PropertiesMap): map of the properties
            algorithm (Algorithm): selected algorithm
            algsmap (AlgorithmsMap): map of all algorithms available

        Returns:
            dict<str, obj>: data object
    """
    # check data types before json conversion
    misc.checkTypeAgainst(type(groupsmap), gm.GroupsMap, __file__)
    misc.checkTypeAgainst(type(resultsmap), rm.ResultsMap, __file__)
    misc.checkTypeAgainst(type(propertiesmap), pm.PropertiesMap, __file__)
    misc.checkInstanceAgainst(algorithm, Algorithm, __file__)
    misc.checkTypeAgainst(type(algsmap), am.AlgorithmsMap, __file__)
    # get json objects
    groupsobj = groupsmap.getJSON()
    resultsobj = resultsmap.getJSON()
    propertiesobj = propertiesmap.getJSON()
    algorithmobj = algorithm.getJSON()
    algorithmsobj = algsmap.getJSON()
    # build data object
    dataobj = {
        "groups": groupsobj,
        "results": resultsobj,
        "properties": propertiesobj,
        "algorithms": {
            "selected": algorithmobj,
            "all": algorithmsobj
        }
    }
    return dataobj


# [Private]
def _generateSuccessMessage(dataobj, messages=[]):
    """
        Generates success message that includes status, code, data object
        and messages list.

        Args:
            dataobj (dict<str, obj>): data object
            messages (list<str>): list of messages

        Returns:
            str: json representation of success message
    """
    # just make sure that messages is a list, if not - reset it to default
    if type(messages) is not ListType:
        messages = []
    # build global object
    obj = {
        "status": "success",
        "code": 200,
        "data": dataobj,
        "messages": messages
    }
    return json.dumps(obj)


# [Private]
def _generateErrorMessage(message, code=400):
    """
        Generates json with error message provided.

        Args:
            code (int): error message code
            message (str): error message

        Returns:
            str: json string with error message
    """
    # build global error object
    obj = {
        "code": int(code),
        "status": "error",
        "data": None,
        "messages": [message]
    }
    return json.dumps(obj)
