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
import os
import json
from types import DictType, StringType
# import classes
import analytics.utils.misc as misc
import analytics.loading.jsonloader as jsl

# global parameters, like manifest name and default directory
_MANIFEST_JSON = "manifest.json"
_DIRECTORY = os.path.join(os.path.dirname(__file__), "datasets")

# Dataset parameters that are used for an parsing object
ID = "id"
NAME = "name"
DESC = "desc"
DISCOVER = "discover"
DATA = "data"
DATA_Groups = "groups"
DATA_Results = "results"
DATA_Properties = "properties"
FILE = "file"
PATH = "path"
TYPE = "type"


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
        self._id = obj[ID]
        self._name = obj[NAME]
        self._desc = obj[DESC]
        self._discover = bool(obj[DISCOVER])
        # files data
        _data = obj[DATA]
        # path and type constants
        # groups file name and type
        _groups_filename = _data[DATA_Groups][FILE]
        _groups_filetype = _data[DATA_Groups][TYPE]
        self._groups = {
            PATH: self._filepath(dr, _groups_filename, _groups_filetype),
            TYPE: _groups_filetype
        }
        # results file name and type
        _results_filename = _data[DATA_Results][FILE]
        _results_filetype = _data[DATA_Results][TYPE]
        self._results = {
            PATH: self._filepath(dr, _results_filename, _results_filetype),
            TYPE: _results_filetype
        }
        self._properties = None
        # if discover is False, specify properties
        if not self._discover:
            _prop_filename = _data[DATA_Properties][FILE]
            _prop_filetype = _data[DATA_Properties][TYPE]
            self._properties = {
                PATH: self._filepath(dr, _prop_filename, _prop_filetype),
                TYPE: _prop_filetype
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

    # [Public]
    def util_testDatasets(self, searchpath=None):
        """
            Collects and tests datasets that are in the folder. Keeps results
            in list for a particular manifest found.

            Args:
                searchpath (str): search path

            Returns:
                dict<str, obj>: result of the testing
        """
        searchpath = searchpath or self._directory
        self.resetToDefault()
        # assign back search path
        self.setSearchPath(searchpath)
        # look for manifests and parse them
        self._findManifests(self._directory)
        # statistics for manifests
        manifest_stats = {}
        for manifestpath in self._manifests.values():
            manifest_stats[manifestpath] = {}
            _exists = os.path.isfile(manifestpath)
            manifest_stats[manifestpath]["manifest"] = _exists
            if _exists:
                try:
                    self._parseManifest(manifestpath)
                    manifest_stats[manifestpath]["dataset"] = True
                except:
                    manifest_stats[manifestpath]["dataset"] = False
        # statistics for datasets
        ds_stats = {}
        for ds in self._datasets.values():
            ds_stats[ds._id] = {}
            ds_stats[ds._id]["groups"] = os.path.isfile(ds._groups[PATH])
            ds_stats[ds._id]["results"] = os.path.isfile(ds._results[PATH])
            if ds._discover:
                continue
            ds_stats[ds._id]["properties"] = os.path.isfile(ds._properties[PATH])

        # stats finished, report statistics
        return {"manifests": manifest_stats, "datasets": ds_stats}

    # [Public]
    def util_checkDatasetsResult(self, obj):
        """
            Checks overall result of the object received from
            "util_testDatasets" and returns bool value that indicates whether
            test is passed or not.

            Args:
                obj (dict<str, obj>): result of the testing

            Returns:
                bool: flag to show whether test is passed or failed
        """
        manfs = obj["manifests"]
        ds = obj["datasets"]
        flag = True
        # test types
        flag = flag and type(manfs) is DictType and type(ds) is DictType
        # test lengths of keys
        flag = flag and len(manfs.keys()) == len(ds.keys())
        # check result of common assertions
        if not flag:
            return flag
        # continue testing of each manifest and dataset
        # check manifests
        mn = [m for manf in manfs.values() for m in manf.values() if not m]
        # check datasets
        dt = [p for dsf in ds.values() for p in dsf.values() if not p]
        return flag and len(mn)==0 and len(dt)==0
