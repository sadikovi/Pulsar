#!/usr/bin/env python

# import libs
import os
import json
from types import DictType, StringType
# import classes
import analytics.utils.misc as misc
import analytics.loading.jsonloader as jsl

# global parameters, like manifest name and default directory
_MANIFEST_JSON = "manifest.json"
_DIRECTORY = os.path.join(os.path.dirname(__file__), "datasets")


class Dataset(object):
    """
        Simple dataset class to hold all the parameters. Converts filenames
        into paths for download by specifying "dr" attribute.

        Attributes:
            _id (str): dataset id
            _name (str): dataset name
            _desc (str): dataset desc
            _discover (bool): dataset isDiscover property
            _groups (dict<str, str>): groups information (path and type)
            _results (dict<str, str>): results information (path and type)
            _properties (dict<str, str>): properties information (path and type)
    """
    def __init__(self, obj, dr):
        misc.checkTypeAgainst(type(obj), DictType, __file__)
        misc.checkTypeAgainst(type(dr), StringType, __file__)
        self._id = obj["id"]
        self._name = obj["name"]
        self._desc = obj["desc"]
        self._discover = bool(obj["discover"])
        self._groups = {
            "path": dr+"/"+obj["data"]["groups"]["file"].replace("/", "_")+ \
                    "."+obj["data"]["groups"]["type"],
            "type": obj["data"]["groups"]["type"]
        }
        self._results = {
            "path": dr+"/"+obj["data"]["results"]["file"].replace("/", "_")+ \
                    "."+obj["data"]["results"]["type"],
            "type": obj["data"]["results"]["type"]
        }
        self._properties = None
        # if discover is False, specify properties
        if not self._discover:
            self._properties = {
                "path": dr+"/"+obj["data"]["properties"]["file"].replace("/", "_")+ \
                        "."+obj["data"]["properties"]["type"],
                "type": obj["data"]["properties"]["type"]
            }

    # [Public]
    def getJSON(self):
        """
            Returns json object.

            Returns:
                dict<str, str>: json representation of Dataset instance
        """
        return {
            "id": self._id,
            "name": self._name,
            "desc": self._desc
        }


class DataManager(object):
    """
        DataManager class helps with datasets maintainance. It searches
        specified directory and collect manifests, then parses them into
        Dataset objects.

        Attributes:
            _manifests (list<str>): list of paths to manifests files
            _datasets (dir<str, Dataset>): map of datasets
            _directory (str): search directory
    """
    def __init__(self):
        self._manifests = []
        self._datasets = {}
        self._directory = _DIRECTORY

    # [Private]
    def _findManifests(self, directory):
        """
            Scans directory and collects manifests paths in _manifests
            attribute.

            Args:
                directory (str): directory to search in
        """
        misc.checkTypeAgainst(type(directory), StringType, __file__)
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == _MANIFEST_JSON:
                    self._manifests.append(os.path.join(root, file))

    # [Private]
    def _parseManifest(self, path):
        """
            Parses manifest that has path specified. Returns True if dataset
            was parsed successfully and added to _datasets dictionary.
            Otherwise, aborts the parsing and returns False.

            Args:
                path (str): path to the manifest file

            Returns:
                bool: status of parsing operation
        """
        # load from path, if it fails, skip it
        dataset = None
        try:
            obj = None
            loader = jsl.JsonLoader(path)
            obj = loader.processData()
            # create dataset
            dataset = Dataset(obj, os.path.dirname(path))
        except:
            dataset = None

        if dataset is None:
            return False
        else:
            self._datasets[dataset._id] = dataset
        return True

    # [Public]
    def loadDatasets(self):
        """
            Loads datasets from _directory path.
        """
        self._manifests = []
        self._datasets = {}
        self._findManifests(self._directory)
        for manifestpath in self._manifests:
            self._parseManifest(manifestpath)

    # [Public]
    def getDatasets(self):
        """
            Returns list of Dataset object collected.

            Returns:
                list<Dataset>: list of Dataset instances
        """
        return self._datasets.values()

    # [Public]
    def getDataset(self, id):
        """
            Returns dataset by id specified. If there is no such id, then
            returns None.

            Args:
                id (str): dataset id

            Returns:
                Dataset: dataset object with id specified
        """
        return self._datasets[id] if id in self._datasets else None

    # [Public]
    def setSearchPath(self, path):
        """
            Sets searching path.

            Args:
                path (str): new searching directory
        """
        self._directory = path

    # [Public]
    def resetToDefault(self):
        """
            Resets instance to default parameters.
        """
        self._directory = _DIRECTORY
        self._manifests = []
        self._datasets = {}
