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
import projectpaths as paths
import analytics.datamanager.datamanager as datamanager
from analytics.loading.loader import Loader
from analytics.loading.jsonloader import JsonLoader
from analytics.loading.xmlloader import XmlLoader


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


# [Public]
def getAllDatasets():
    """
        Returns list with all datasets available. If something fails, return
        empty list.

        Returns:
            str: json string of available datasets
    """
    try:
        obj = [x.getJSON() for x in _datamanager.getDatasets()]
        return json.dumps(obj)
    except:
        return json.dumps([])


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
        """
        jsonobj = _requestData(dataset, query)
        jsonstring = _generateSuccessMessage(jsonobj)
        """
    except ex.AnalyticsBaseException as e:
        jsonstring = _generateErrorMessage(e._errmsg)
    return jsonstring


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
            str: json representation of success message
    """
    misc.checkTypeAgainst(type(messages), ListType, __file__)
    # build global object
    obj = {
        "status": "success",
        "code": 200,
        "data": dataobj,
        "messages": messages
    }
    return json.dumps(obj)


# [Private]
def _generateErrorMessage(messages, code=400):
    """
        Generates json with error message provided.

        Args:
            messages (list<str>): error message
            code (int): error message code

        Returns:
            str: json string with error message
    """
    misc.checkTypeAgainst(type(messages), ListType, __file__)
    # build global error object
    obj = {
        "code": int(code),
        "status": "error",
        "data": None,
        "messages": messages
    }
    return json.dumps(obj)
