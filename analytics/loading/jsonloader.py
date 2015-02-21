# import libs
import json
from types import StringType
# import classes
import analytics.loading.loader as l
import analytics.utils.misc as misc


class JsonLoader(l.Loader):
    """
        JsonLoader class is a subclass of Loader that provides actual interface
        to load data from json file. It overrides methods @prepareDataFrom and
        @processData and takes attribute for file path.

        Example of json file:
            [
                {"id": "1", "name": "1", "desc": "1", "parent": null},
                {"id": "2", "name": "2", "desc": "2", "parent": "1"},
                {"id": "3", "name": "3", "desc": "3", "parent": "1"},
                {"id": "4", "name": "4", "desc": "4", "parent": "2"},
                {"id": "5", "name": "5", "desc": "5", "parent": "2"}
            ]

        Attributes:
            _filepath (str): json file path
    """

    def __init__(self, filepath):
        self._filepath = filepath

    @classmethod
    def prepareDataFrom(cls, filepath):
        """
            Class method to instantiate JsonLoader instance. Takes file path
            as an argument and checks against StringType.

            Args:
                filepath (str): json file path
        """
        misc.checkTypeAgainst(type(filepath), StringType)
        return cls(filepath)

    # [Public]
    def processData(self):
        """
            Process data from the file specified as _filepath attribute.
            Returns standard dictionary / list as json object, or raises
            exception, if file does not exist or json is invalid.

            Returns:
                dict<str, object> / list<object>: json object from the file
        """
        file = open(self._filepath)
        jsonObject = json.load(file)
        file.close()
        return jsonObject
