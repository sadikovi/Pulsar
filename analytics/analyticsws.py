# import libs
import json
from types import StringType, ListType
import os
# import classes
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
from analytics.algorithms.algorithm import Algorithm

# project directory
ANALYTICS_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# Authorised email list
#[Private]
_EMAIL_LIST = [
    "test@example.com"
]

# datasets available
# [Private]
_DATASETS = [
    {
        "id": "test",
        "name": "Test set",
        "desc": "Test set",
        "path": "/datasets/test",
        "type": "json",
        "discover": False
    }
]


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
        jsonstr = json.dumps(_DATASETS)
    except:
        jsonstr = "[]"
    return jsonstr


# [Public]
def requestData(datasetId, query="", datasets=_DATASETS):
    """
        Public method to request data, has error handling. Returns data json,
        if everything is okay, otherwise returns error json.

        Args:
            datasetId (str): id of a particular dataset
            query (str): select query for data
            datasets (list<dict>): list of datasets

        Returns:
            str: json string of results
    """
    jsonstring = ""
    try:
        jsonstring = _requestData(datasetId, query, datasets)
    except BaseException as e:
        jsonstring = generateErrorMessage(str(e))
    return jsonstring


# [Private]
# requesting data for dataset
def _requestData(datasetId, query="", datasets=_DATASETS):
    """
        Collects data from dataset and applies query to select a particular
        results. Empty query means default selection.

        Args:
            datasetId (str): id of a particular dataset
            query (str): select query for data
            datasets (list<dict>): list of datasets

        Returns:
            str: json string of results
    """
    # map dataset parameters
    ID = "id"; NAME = "name"; PATH = "path"; TYPE = "type";
    DISCOVER = "discover"
    # check arguments
    misc.checkTypeAgainst(type(datasetId), StringType)
    misc.checkTypeAgainst(type(query), StringType)
    misc.checkTypeAgainst(type(datasets), ListType)
    # trim arguments
    datasetId = datasetId.strip(); query = query.strip();
    # find that ther is actual dataset stored
    list = [x for x in datasets if x[ID] == datasetId]
    listlen = len(list)
    # check dataset
    if listlen > 1:
        # more than 1 dataset - ambiguity error
        raise StandardError("Datasets ambiguity (more than 1 dataset with id)")
    elif listlen == 0:
        # no datasets - error
        raise StandardError("No such dataset")
    # everything is okay
    # extract dataset and get path
    dataset = list[0]
    path = dataset[PATH]; isDiscover = dataset[DISCOVER]
    # datatype to load a particular loader
    datatype = dataset[TYPE]
    groups = None; results = None; properties = None
    # create loader, if something is wrong it will raise an exception
    loader = _loaderForDatatype(datatype, "")
    # extract data: groups, results, properties
    groups = loader.processData(_pathFor(path, "groups", datatype))
    results = loader.processData(_pathFor(path, "results", datatype))
    if not isDiscover:
        _props = loader.processData(_pathFor(path, "properties", datatype))
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
    flag = selector.startFiltering(groupsmap, resmap, propsmap, algsmap)
    # analyse using algorithms map
    resmap = analyser.analyseUsingMap(algsmap, resmap, propsmap)
    # get last selected algorithm that has been used by this instance
    selectedAlg = analyser.getSelectedAlgorithm()
    # now we have everything filtered and ranked
    # prepare json object to send data back
    jsonstring = generateData(groupsmap, resmap, propsmap, selectedAlg)
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
        raise StandardError(msg)

# [Private]
def _pathFor(path, file, fileformat):
    """
        Returns full path from path, file and fileformat.

        Args:
            path (str): path to the folder
            file (str): file in the folder
            fileformat (str): file format

        Returns:
            str: full path to the file
    """
    misc.checkTypeAgainst(type(path), StringType)
    misc.checkTypeAgainst(type(file), StringType)
    misc.checkTypeAgainst(type(fileformat), StringType)
    # remove slashes
    path = path.strip("/")
    file = file.strip("/")
    return "%s/%s/%s.%s" %(ANALYTICS_DIRECTORY, path, file, fileformat)


# [Private]
def generateErrorMessage(msg=""):
    """
        Generates json with error message provided.

        Args:
            msg (str): error message

        Returns:
            str: json string with error message
    """
    # build global error object
    obj = { "status": "error", "data": None, "message": msg }
    return json.dumps(obj)


# [Private]
def generateData(groupsmap, resultsmap, propertiesmap, algorithm):
    """
        Generates json data from maps and algorithm, combines them together to
        return back.

        Args:
            groupsmap (GroupsMap): map of the groups
            resultsmap (ResultsMap): map of the results
            propsmap (PropertiesMap): map of the properties
            algorithm (Algorithm): selected algorithm

        Returns:
            str: json string with data
    """
    # check data types before json conversion
    try:
        misc.checkTypeAgainst(type(groupsmap), gm.GroupsMap)
        misc.checkTypeAgainst(type(resultsmap), rm.ResultsMap)
        misc.checkTypeAgainst(type(propertiesmap), pm.PropertiesMap)
        misc.checkInstanceAgainst(algorithm, Algorithm)
    except BaseException as e:
        return generateErrorMessage(str(e))
    # get json objects
    groupsobj = groupsmap.getJSON()
    resultsobj = resultsmap.getJSON()
    propertiesobj = propertiesmap.getJSON()
    algorithmobj = algorithm.getJSON()
    # build data object
    dataobj = {
        "groups": groupsobj,
        "results": resultsobj,
        "properties": propertiesobj,
        "algorithm": algorithmobj
    }
    # build global object
    obj = { "status": "success", "data": dataobj, "message": None }
    return json.dumps(obj)
