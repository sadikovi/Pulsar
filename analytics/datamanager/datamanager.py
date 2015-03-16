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


class DKeys(object):
    """
        Class DKeys is a set of constant parameter names for attributes
        of the parsing object.
    """
    pass
# Dataset parameters that are used for an parsing object
DKeys.ID = "id"
DKeys.NAME = "name"
DKeys.DESC = "desc"
DKeys.DISCOVER = "discover"
DKeys.DATA = "data"
DKeys.DATA_Groups = "groups"
DKeys.DATA_Results = "results"
DKeys.DATA_Properties = "properties"
DKeys.FILE = "file"
DKeys.TYPE = "type"


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
        self._id = obj[DKeys.ID]
        self._name = obj[DKeys.NAME]
        self._desc = obj[DKeys.DESC]
        self._discover = bool(obj[DKeys.DISCOVER])
        # files data
        _data = obj[DKeys.DATA]
        # path and type constants
        c_path = "path"; c_type = "type"
        # groups file name and type
        _groups_filename = _data[DKeys.DATA_Groups][DKeys.FILE]
        _groups_filetype = _data[DKeys.DATA_Groups][DKeys.TYPE]
        self._groups = {
            c_path: self._filepath(dr, _groups_filename, _groups_filetype),
            c_type: _groups_filetype
        }
        # results file name and type
        _results_filename = _data[DKeys.DATA_Results][DKeys.FILE]
        _results_filetype = _data[DKeys.DATA_Results][DKeys.TYPE]
        self._results = {
            c_path: self._filepath(dr, _results_filename, _results_filetype),
            c_type: _results_filetype
        }
        self._properties = None
        # if discover is False, specify properties
        if not self._discover:
            _prop_filename = _data[DKeys.DATA_Properties][DKeys.FILE]
            _prop_filetype = _data[DKeys.DATA_Properties][DKeys.TYPE]
            self._properties = {
                c_path: self._filepath(dr, _prop_filename, _prop_filetype),
                c_type: _prop_filetype
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

    # [Private]
    def _filepath(self, directory, filename, filetype):
        """
            Returns full file path for specified directory, file name and file
            type.

            Args:
                directory (str): directory
                filename (str): file name
                filetype (str): file type

            Returns:
                str: full file path
        """
        # replace any "/" on "_"
        filename = filename.replace("/", "_")
        return os.path.join(directory, "%s.%s"%(filename, filetype))


class DataManager(object):
    """
        DataManager class helps with datasets maintainance. It searches
        specified directory and collect manifests, then parses them into
        Dataset objects.

        Attributes:
            _manifests (dir<str, str>): map of dirs and manifest file paths
            _datasets (dir<str, Dataset>): map of datasets
            _directory (str): search directory
    """
    def __init__(self):
        # declare attributes
        self._manifests = {}; self._datasets = {}; self._directory = ""
        self.resetToDefault()

    # [Private]
    def _findManifests(self, directory):
        """
            Scans directory and collects manifests paths into _manifests
            attribute.

            Args:
                directory (str): directory to search in
        """
        misc.checkTypeAgainst(type(directory), StringType, __file__)
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file == _MANIFEST_JSON:
                    self._manifests[root] = os.path.join(root, file)

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
    def loadDatasets(self, searchpath=None):
        """
            Loads datasets from _directory path.

            Args:
                searchpath (str): search path for datasets
        """
        # assign search path or use it to save previous path
        searchpath = searchpath or self._directory
        # clean previous datasets and manifests info
        self.resetToDefault()
        # assign back search path
        self.setSearchPath(searchpath)
        # look for manifests and parse them
        self._findManifests(self._directory)
        for manifestpath in self._manifests.values():
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
        self._manifests = {}
        self._datasets = {}
