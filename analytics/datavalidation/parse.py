# import libs
import uuid
from types import DictType, StringType
# import classes
import analytics.datavalidation.exceptions.checkerror as c


class Parse(object):
    """
        Class Parse is built for parsing a json object into Group, Property
        or Result object by retrieving relevant to the class parameters. It
        uses lists for some common attributes names to search attributes (id,
        name, desc, group, parent, and sample).

        Attributes:
            _object (dict<str, object>): object to keep reference to
            _primaryKeys (list<str>): a list of primary attributes, such as
                                            id, name, desc and etc.
    """

    # Arrays for primary attributes
    KEY_ID = ['id', 'uuid', 'Id', 'ID']
    KEY_NAME = ['name', 'Name', 'NAME']
    KEY_DESC = ['desc', 'DESC', 'description', 'DESCRIPTION']
    KEY_GROUP = ['group', 'parent', 'Group', 'Parent', 'GROUP', 'PARENT']
    KEY_PARENT = ['parent', 'Parent', 'PARENT']
    KEY_SAMPLE = ['sample', 'value']

    def __init__(self, object):
        self.updateInstance(object)

    # [Private]
    def _resetParse(self):
        """
            Resets instance attributes to default values. In this case
            _object will be None, _primaryKeys will be an empty list.
        """
        self._object = None
        self._primaryKeys = []

    # [Private]
    def _getValueForKeyArray(self, array):
        """
            Returns value for a key that is specified as a list of most likely
            attribute names. Once key is occured in _object and list of key
            values, the value is returned. If key is not found then None is
            returned.

            Args:
                array (list<str>): list of predicted values for the key

            Returns:
                object: value for a key found in a set of possible keys
        """
        if (self._object is None): raise c.CheckError("object", "None")
        for key in array:
            if key in self._object:
                self._primaryKeys.append(key)
                return self._object[key]
        return None

    # [Public]
    def updateInstance(self, object):
        """
            Updates Parse instance, particularly _object reference. Useful for
            reusing the same object for different dictionaries of data.

            Args:
                object (dict<str, object>): object to update reference to
        """
        if type(object) is not DictType:
            raise c.CheckError("<type 'dict'>", str(type(object)))
        self._resetParse()
        self._object = object

    # [Public]
    def getExternalId(self):
        """
            Returns external system id using KEY_ID list of possible key
            values. If id is found returns string, otherwise, None.

            Returns:
                str: external system id
        """
        return self._getValueForKeyArray(Parse.KEY_ID)

    @classmethod
    def guidBasedId(self, id=''):
        """
            Generates unique guid that can be used as a internal id. Takes @id
            string as parameter (can be empty) and generates hex value for
            guid.

            Args:
                id (str): id string to use to generate part of guid

            Returns:
                str: unique random uuid as internal guid
        """
        id = uuid.uuid3(uuid.NAMESPACE_DNS, id).hex \
            if type(id) == StringType and len(id) > 0 else uuid.uuid4().hex
        return str(uuid.uuid4()) + '-' + id

    # [Public]
    def getName(self):
        """
            Returns name for a specified list of possible key values. If found,
            returns string, otherwise, None.

            Returns:
                str: name of the object
        """
        return self._getValueForKeyArray(Parse.KEY_NAME)

    # [Public]
    def getDesc(self):
        """
            Returns description for a specified list of possible key values. If
            found, returns a string with description, otherwise, None.

            Returns:
                str: description of the object
        """
        return self._getValueForKeyArray(Parse.KEY_DESC)

    # [Public]
    def getGroup(self):
        """
            Returns group id for a list with possible key values. Returns
            string, if found, otherwise, None.

            Returns:
                str: object's group
        """
        return self._getValueForKeyArray(Parse.KEY_GROUP)

    # [Public]
    def getParent(self):
        """
            Returns parent id from an object. Uses list of possible key values
            to retrieve value. Returns string, if found, otherwise, None.

            Returns:
                str: parent id of the object
        """
        return self._getValueForKeyArray(Parse.KEY_PARENT)

    # [Public]
    def getSample(self):
        """
            Returns sample value for a list with possible keys. Sample is used
            by Property objects to determine the type of property.
            Returns string, if found, otherwise None.

            Returns:
                str: sample value of the object
        """
        return self._getValueForKeyArray(Parse.KEY_SAMPLE)

    # [Public]
    'excluding id, name, desc, group and other primary attributes'
    def getSecondaryProperties(self):
        """
            Returns dictionary with secondary properties. That excludes id,
            name, desc, group, and etc. Better to run this method after all the
            primary properties have been checked.

            Returns:
                dict<str, object>: dictionary with secondary properties.
        """
        if len(self._primaryKeys) == 0:
            return self._object
        secondaryKeys = list(set(self._object.keys())-set(self._primaryKeys))
        a = {}
        for key in secondaryKeys:
            a[key] = self._object[key]
        return a
